#!/usr/bin/env python3
"""review_index.py —— workflow-reviews 复盘索引生成器（DSH 提供，放置于仓库 tools/）
用法（仓库根目录）:
    python -I tools/review_index.py
输出:
    reports/INDEX.md         总索引（人读）
    reports/index/*.csv      机器可读（轮次/建议/未闭环/证据/跨轮重复）
只读 review.json，不改任何 review.md；不联网。
"""
import csv, datetime, glob, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RPT = os.path.join(ROOT, 'reports')
OUT = os.path.join(RPT, 'index')
NOW = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
os.makedirs(OUT, exist_ok=True)


def short(s, n=90):
    s = ' '.join(str(s or '').split())
    return s[:n] + ('…' if len(s) > n else '')


def metric(d, *names):
    want = set(names)
    for m in d.get('metrics') or []:
        if str(m.get('name', '')).strip() in want:
            return m.get('value')
    return None


rounds = []
for name in sorted(os.listdir(RPT)):
    p = os.path.join(RPT, name)
    j = os.path.join(p, 'review.json')
    if os.path.isdir(p) and os.path.exists(j):
        try:
            rounds.append({'dir': name, 'json': json.load(open(j, encoding='utf-8'))})
        except Exception as e:
            print('解析失败', name, e)

tracked = set()
try:
    o = subprocess.run(['git', '-C', ROOT, 'ls-files', 'reports/'], capture_output=True, timeout=30)
    for line in o.stdout.decode('utf-8', 'replace').splitlines():
        parts = line.strip().split('/')
        if len(parts) >= 2 and parts[0] == 'reports':
            tracked.add(parts[1])
except Exception:
    pass

rows, all_recs, all_rem = [], [], []
for r in rounds:
    d = r['json']; q = d.get('quality') or {}; recs = d.get('recommendations') or []
    rows.append({
        '轮次目录': r['dir'], 'round_id': d.get('round_id', ''),
        '入库状态': '已提交' if r['dir'] in tracked else '未提交',
        '质量状态': q.get('status', ''),
        '完成项数': len(q.get('completed') or []), '剩余项数': len(q.get('remaining') or []),
        '建议数': len(recs),
        '有效分钟': metric(d, '有效时间'), '墙钟分钟': metric(d, '墙钟时间', '墙钟'),
        '工具调用': metric(d, '工具调用'), '失败调用': metric(d, '失败的调用'),
        '任务摘要': short(d.get('task_summary'), 120),
    })
    for x in recs:
        all_recs.append({'轮次': r['dir'], 'id': x.get('id', ''), 'owner': x.get('owner', ''),
                         'status': x.get('status', ''), 'action': x.get('action', ''),
                         'next_check': x.get('next_check', '')})
    for rem in q.get('remaining') or []:
        all_rem.append({'轮次': r['dir'], '剩余事项': str(rem)})

ev_rows = []


def extract_paths(s):
    out = []
    for part in re.split(r'[，,；;、（）()\s]+', str(s)):
        m = re.match(r'^([A-Za-z]:/[^，,；;、（）()\s"“”]+)', part)
        if m:
            out.append(m.group(1).rstrip('。.'))
    return out


def path_exists(raw):
    p = raw.replace('/', '\\')
    if '*' in p or '?' in p:
        return len(glob.glob(p)) > 0
    return os.path.exists(p)


for r in rounds:
    for ev in r['json'].get('evidence') or []:
        for raw in extract_paths(ev):
            ev_rows.append({'轮次': r['dir'], '证据': str(ev), '路径': raw,
                            '存在': '是' if path_exists(raw) else '否'})

rec_by_id = {}
for x in all_recs:
    rec_by_id.setdefault(x['id'], []).append(x)
recurring = {k: v for k, v in rec_by_id.items() if len({y['轮次'] for y in v}) > 1}

anomalies = []
QUALITY_OK = ('passed', 'partial', 'failed', 'unverified')
REC_OK = ('proposed', 'adopted', 'verified', 'rejected')
for r in rounds:
    d = r['json']; q = d.get('quality') or {}
    if q.get('status') not in QUALITY_OK:
        anomalies.append((r['dir'], '质量状态取值异常', q.get('status')))
    if q.get('status') == 'passed' and (q.get('remaining') or []):
        anomalies.append((r['dir'], 'passed 但 remaining 非空', ''))
    for x in d.get('recommendations') or []:
        if x.get('status') not in REC_OK:
            anomalies.append((r['dir'], '建议状态取值异常', f"{x.get('id')}={x.get('status')}"))


def dump(name, fields, data):
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for x in data:
            w.writerow(x)


dump('reviews-index.csv', list(rows[0].keys()), rows)
dump('recommendations.csv', ['轮次', 'id', 'owner', 'status', 'action', 'next_check'], all_recs)
dump('open-remaining.csv', ['轮次', '剩余事项'], all_rem)
dump('evidence-check.csv', ['轮次', '证据', '路径', '存在'], ev_rows)
if recurring:
    rr = []
    for k, v in sorted(recurring.items()):
        for y in v:
            rr.append({'id': k, '轮次': y['轮次'], 'status': y['status'], 'owner': y['owner'],
                       'action': y['action'], 'next_check': y['next_check']})
    dump('recurring-recs.csv', ['id', '轮次', 'status', 'owner', 'action', 'next_check'], rr)

open_recs = [x for x in all_recs if (x['status'] or '') == 'proposed']
by_owner = {}
for x in open_recs:
    by_owner.setdefault(x['owner'] or '未指定', []).append(x)

L = [f'# workflow-reviews 总索引（{NOW} 由 `tools/review_index.py` 生成）', '',
     f'- 共 {len(rows)} 轮；校验与一致性由 `tools/workflow_review.py` 另行负责，本脚本只做聚合。', '',
     '## 1. 全部轮次', '',
     '| 轮次 | 入库 | 质量 | 完成/剩余 | 建议 | 有效分钟 | 墙钟分钟 | 工具调用 | 失败调用 | 任务 |',
     '|---|---|---|---|---|---|---|---|---|---|']
for x in rows:
    L.append(f"| [{x['round_id'] or x['轮次目录']}]({x['轮次目录']}/review.md) | {x['入库状态']} | {x['质量状态']} | "
             f"{x['完成项数']}/{x['剩余项数']} | {x['建议数']} | "
             f"{x['有效分钟'] if x['有效分钟'] is not None else '-'} | "
             f"{x['墙钟分钟'] if x['墙钟分钟'] is not None else '-'} | "
             f"{x['工具调用'] if x['工具调用'] is not None else '-'} | "
             f"{x['失败调用'] if x['失败调用'] is not None else '-'} | {short(x['任务摘要'], 50)} |")
untracked = [x for x in rows if x['入库状态'] == '未提交']
if untracked:
    L += ['', '> ⚠️ 未提交轮次：' + '、'.join(x['轮次目录'] for x in untracked)]
L += ['', '## 2. 未闭环事项', '']
L.append(f'### 2.1 proposed 建议（{len(open_recs)} 条）')
L.append('')
for owner, items in sorted(by_owner.items()):
    L.append(f'**{owner}**')
    L.append('')
    for x in items:
        L.append(f"- `{x['id']}`（{x['轮次']}）：{short(x['action'], 110)}")
    L.append('')
L.append(f'### 2.2 quality.remaining（{len(all_rem)} 条）')
L.append('')
for x in all_rem:
    L.append(f"- [{x['轮次']}] {x['剩余事项']}")
L += ['', '## 3. 证据路径', '']
exists = [x for x in ev_rows if x['存在'] == '是']
missing = [x for x in ev_rows if x['存在'] == '否']
L.append(f'- 绝对路径 {len(ev_rows)} 条：存在 {len(exists)}，不存在 {len(missing)}')
if missing:
    L += ['', '| 轮次 | 缺失路径 |', '|---|---|']
    for x in missing[:40]:
        L.append(f"| {x['轮次']} | `{x['路径']}` |")
L += ['', '## 4. 反复重申的建议', '']
if recurring:
    L += ['| 编号 | 轮次 | 状态 | 内容 |', '|---|---|---|---|']
    for k, v in sorted(recurring.items(), key=lambda kv: -len(kv[1])):
        L.append(f"| {k} | {len(v)} | {', '.join(sorted({y['status'] for y in v}))} | {short(v[0]['action'], 80)} |")
else:
    L.append('（无）')
L += ['', '## 5. 异常', '']
if anomalies:
    for a in anomalies:
        L.append(f'- [{a[0]}] {a[1]}：{a[2]}')
else:
    L.append('schema 关键字段检查：无异常。')
open(os.path.join(RPT, 'INDEX.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print(f'已生成 reports/INDEX.md，{len(rows)} 轮；CSV 在 reports/index/')
