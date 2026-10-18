"""Validate one round's evidence record and render it; no model or network calls."""
import argparse
from datetime import datetime
import json
import math
from pathlib import Path
import re


def timestamp(value):
    if value is None:
        return None
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError('Timestamps must include a timezone')
    return dt


def nonnegative(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def analyse(data):
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported schema_version')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*', data['round_id']):
        raise ValueError('Use YYYY-MM-DD-task-name for round_id')
    for field in ('task_summary', 'workflow_version'):
        if not isinstance(data[field], str) or not data[field].strip():
            raise ValueError('Missing ' + field)
    start, end = timestamp(data['started_at']), timestamp(data['measurement_cutoff_at'])
    wall = (end-start).total_seconds() if start and end else None
    if wall is not None and wall < 0:
        raise ValueError('Measurement cutoff precedes start')
    quality = data['quality']
    if quality['status'] not in ('passed', 'partial', 'failed', 'unverified'):
        raise ValueError('Invalid quality status')
    if not quality['acceptance']:
        raise ValueError('Acceptance criteria are required')
    for field in ('completed', 'remaining', 'acceptance'):
        if not isinstance(quality[field], list):
            raise ValueError('quality.' + field + ' must be a list')
    if quality['status'] == 'passed' and quality['remaining']:
        raise ValueError('Passed rounds cannot have unmet acceptance criteria')
    for field in ('metrics', 'observations', 'recommendations', 'evidence', 'limits'):
        if not isinstance(data[field], list):
            raise ValueError(field + ' must be a list')
    for metric in data['metrics']:
        if not metric['name'] or not metric['basis'] or not metric['unit']:
            raise ValueError('Every metric needs a name, unit and basis')
        if metric['value'] is not None and not nonnegative(metric['value']):
            raise ValueError('Metric values must be finite nonnegative numbers or null')
    for change in data['recommendations']:
        for field in ('id', 'action', 'owner', 'status', 'next_check'):
            if not change.get(field):
                raise ValueError('Recommendation missing ' + field)
        if change['status'] not in ('proposed', 'adopted', 'verified', 'rejected'):
            raise ValueError('Invalid recommendation status')
    if not data['evidence']:
        raise ValueError('At least one evidence reference is required')
    result = {'wall_seconds': wall, 'observed_time_change_pct': None,
              'verdict': '证据不足：没有合格的同条件基线，不能判断净提效。',
              'causal_claim': '未建立；单轮观察或单次配对不能证明普遍因果收益。'}
    pair = data.get('comparison')
    if pair is not None:
        base = pair['baseline']
        for value in (base['wall_seconds'],):
            if not nonnegative(value) or value == 0:
                raise ValueError('Baseline time must be positive and finite')
        if not base.get('evidence'):
            raise ValueError('Baseline evidence is required')
        matches = all(pair['current'].get(k) and pair['current'][k] == base.get(k)
                      for k in ('task_fingerprint', 'acceptance_fingerprint',
                                'environment_fingerprint', 'protocol_id'))
        if matches and quality['status'] == 'passed' and base.get('quality_status') == 'passed' and wall is not None:
            pct = 100 * (base['wall_seconds']-wall) / base['wall_seconds']
            result['observed_time_change_pct'] = round(pct, 3)
            direction = '更快' if pct > 0 else '更慢' if pct < 0 else '相同'
            result['verdict'] = '这一个合格配对的观察耗时' + direction + '；不外推为普遍提效。'
        else:
            result['verdict'] = '不可比：质量门槛、任务、环境或比较协议不一致/缺失。'
    return result


def render(data):
    result = analyse(data)
    lines = ['# ' + data['round_id'] + ' 工作流复盘', '', data['task_summary'], '',
             '**结论：' + result['verdict'] + '**', '', result['causal_claim'], '',
             '- 工作流：' + data['workflow_version'],
             '- 验收状态：' + data['quality']['status'],
             '- 开始：' + str(data['started_at']),
             '- 测量截止：' + str(data['measurement_cutoff_at']),
             '- 墙钟秒数：' + str(result['wall_seconds']),
             '- 合格配对耗时变化（%）：' + str(result['observed_time_change_pct']), '',
             '## 实测数据', '', '| 指标 | 值 | 单位 | 口径 |', '|---|---:|---|---|']
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ')
    for m in data['metrics']:
        value = '未知' if m['value'] is None else m['value']
        lines.append('| ' + ' | '.join(cell(v) for v in (m['name'], value, m['unit'], m['basis'])) + ' |')
    for title, items in [('验收条件', data['quality']['acceptance']),
                         ('已完成', data['quality']['completed']), ('未完成', data['quality']['remaining']),
                         ('收益与损耗观察', data['observations'])]:
        lines.extend(['', '## ' + title, ''] + ['- ' + str(v) for v in items or ['无记录']])
    lines.extend(['', '## 修改建议及下一轮验收', ''])
    for c in data['recommendations']:
        lines.append(f"- **{c['id']} [{c['status']}]** {c['action']}；负责人：{c['owner']}；下次检查：{c['next_check']}")
    for title, items in [('证据', data['evidence']), ('限制', data['limits'])]:
        lines.extend(['', '## ' + title, ''] + ['- ' + str(v) for v in items])
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.record.read_text(encoding='utf-8-sig'))
        output = render(data)
        destination = args.record.with_suffix('.md')
        destination.write_text(output, encoding='utf-8')
        print(json.dumps(analyse(data), ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, str(exc) + '\n')
