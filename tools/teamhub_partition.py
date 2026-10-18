"""Split an existing TeamHub v1 into project databases, retaining a frozen source and backup."""
import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
from inspect import cleandoc
import json
from pathlib import Path
import re
import sqlite3
import sys
import uuid

if __package__:
    from .studio_runtime.teamhub import ROOT, TeamHub, initialize
else:
    from studio_runtime.teamhub import ROOT, TeamHub, initialize


def install(hub_dir, expected_cli_sha, studio_root=ROOT):
    hub=Path(hub_dir).resolve(strict=True)
    studio=Path(studio_root).resolve(strict=True)
    source=hub/'teamhub.db'; old_cli=hub/'teamdb.py'
    if hashlib.sha256(old_cli.read_bytes()).hexdigest()!=expected_cli_sha:
        raise ValueError('Existing TeamHub CLI changed; inspect current work before installing')
    if (hub/'catalog.json').exists() or (hub/'projects').exists():
        raise ValueError('Catalog or project directory already exists; reconcile instead of re-splitting')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]
    backup_dir=hub/'backups'/stamp
    backup_dir.mkdir(parents=True)
    stage=hub/('.partition-'+stamp); stage.mkdir()
    counts={}; partitions={}; started=datetime.now(timezone.utc).isoformat()
    with closing(sqlite3.connect(source.as_uri()+'?mode=rw',uri=True,timeout=5)) as live:
        with live:
            live.execute('BEGIN IMMEDIATE')
            if live.execute('PRAGMA user_version').fetchone()[0] not in (0,1):
                raise ValueError('Only an unpartitioned v1 source is supported; inspect current schema')
            saved=TeamHub(source).backup(backup_dir/'teamhub-v1.db')
            for name in ('teamdb.py','schema.sql','README.md','AGENT-GUIDE.md'):
                path=hub/name
                if path.is_file(): (backup_dir/name).write_bytes(path.read_bytes())
            with closing(sqlite3.connect(Path(saved['path']).as_uri()+'?mode=ro',uri=True)) as snapshot:
                snapshot.row_factory=sqlite3.Row
                tables=[r[0] for r in snapshot.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
                projects=[dict(r) for r in snapshot.execute('SELECT * FROM projects ORDER BY code')]
                if not projects: raise ValueError('No projects to partition')
                catalog={'schema_version':1,'created_at':started,'projects':[],
                         'roles':{'dsh':'来源采集、去重、分类与证据整理',
                                  'codex':'实现、数据库维护、测试和集成',
                                  'opus':'方案设计、独立评审与验收'},
                         'role_policy':'Default responsibilities; current owner instructions take precedence. Labels are not authentication.'}
                columns={t:[r[1] for r in snapshot.execute('PRAGMA table_info("'+t.replace('"','""')+'")')] for t in tables}
                for t in tables:
                    if not re.fullmatch('[a-z_]+',t): raise ValueError('Unexpected table name')
                    counts[t]=snapshot.execute(f'SELECT count(*) FROM {t}').fetchone()[0]
                    if 'project_id' in columns[t] and snapshot.execute(f'SELECT count(*) FROM {t} WHERE project_id IS NULL OR project_id NOT IN (SELECT id FROM projects)').fetchone()[0]:
                        raise ValueError('Unassigned rows need owner review before partition: '+t)
                project_stage=stage/'projects';project_stage.mkdir()
                for project in projects:
                    code=project['code']
                    if not re.fullmatch('[A-Z0-9][A-Z0-9_-]{0,63}',code): raise ValueError('Unsafe project code')
                    folder=project_stage/code;folder.mkdir(); db_path=folder/'teamhub.db'
                    initialize(db_path); project_counts={}
                    with closing(sqlite3.connect(db_path)) as target:
                        with target:
                            actual_tables={r[0] for r in target.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")}
                            if actual_tables!=set(tables): raise ValueError('Unexpected v1 tables; refusing to discard them')
                            for table in tables:
                                if [r[1] for r in target.execute(f'PRAGMA table_info({table})')]!=columns[table]:
                                    raise ValueError('Schema changed; inspect '+table)
                                where=' WHERE id=?' if table=='projects' else ' WHERE project_id=?' if 'project_id' in columns[table] else ''
                                rows=snapshot.execute(f'SELECT * FROM {table}'+where,(project['id'],) if where else ()).fetchall()
                                target.executemany(f'INSERT INTO {table} VALUES('+','.join('?' for _ in columns[table])+')',rows)
                                project_counts[table]=len(rows)
                    TeamHub(db_path).migrate(backup_dir/(code+'-v1.db'))
                    # Map only unambiguous existing types, never infer a video's technical topic.
                    if code == 'CRAZY-CIRCUIT':
                        with closing(sqlite3.connect(db_path)) as categorized:
                            with categorized:
                                mappings=[('x_teams', '02', '国奖与赛区数据',None,None),
                                          ('x_repos','03','开源源码与仓库',None,None),
                                          ('sources','03','开源源码与仓库','category','repo'),
                                          ('sources','10','风险与陷阱','category','unreliable')]
                                mappings += [(t,'08','协作与交接',None,None) for t in ('tasks','handoffs','reviews')]
                                mappings += [('params','01','赛事规则与评分','category',v) for v in ('rules','weight')]
                                mappings += [('params','04','硬件选型与电路','category',v) for v in ('camera','driver','encoder','imu','mcu')]
                                for table,cat,name,field,value in mappings:
                                    found=categorized.execute('SELECT id FROM project_categories WHERE project_id=? AND code=? AND name=?',(project['id'],cat,name)).fetchall()
                                    if len(found)!=1: continue
                                    condition=' AND '+field+'=?' if field else ''
                                    categorized.execute(f'''INSERT OR IGNORE INTO record_categories
                                        SELECT project_id,?,CAST(id AS TEXT),? FROM {table} WHERE project_id=?'''+condition,
                                        [table,found[0][0],project['id']]+([value] if field else []))
                    with closing(sqlite3.connect(db_path)) as verify:
                        if verify.execute('PRAGMA integrity_check').fetchone()[0]!='ok': raise ValueError('Partition integrity failure')
                        if verify.execute('SELECT count(*) FROM projects').fetchone()[0]!=1: raise ValueError('Project isolation failure')
                    partitions[code]=project_counts
                    catalog['projects'].append({'code':code,'name':project['name'],'database':f'projects/{code}/teamhub.db'})
                for table in tables:
                    if table=='projects' or 'project_id' in columns[table]:
                        if sum(v[table] for v in partitions.values())!=counts[table]: raise ValueError('Row reconciliation failed: '+table)
                wrapper=("# Shared TeamHub entry; maintained in the workflow source repository.\n"
                         "import runpy, sys\nfrom pathlib import Path\n"
                         f"root=Path({str(studio)!r})\n"
                         "sys.path.insert(0,str(root/'tools'))\n"
                         "if '--config' not in sys.argv and '--db' not in sys.argv:\n"
                         "    sys.argv[1:1]=['--config',str(Path(__file__).resolve().parent/'client.json')]\n"
                         "runpy.run_path(str(root/'tools/teamdb.py'),run_name='__main__')\n")
                guide='''# TeamHub：三个 AI 的统一入口

        从此每个项目使用独立数据库，位置见 catalog.json；旧 teamhub.db 已冻结，只留作历史证据。
        不要再写旧总库或它的镜像，不要让不同项目共享一个可写库。

        - DeepSeek / dsh：采集、去重、分类、来源与证据；不替代最终评审。
        - Codex：实现、测试、维护数据库和集成。
        - Opus：方案设计、独立评审和验收。
        - 当前用户指令可调整分工；身份标签不是权限认证。

        先 projects，再 context --project 项目代码；收件箱 inbox --project 项目代码 --agent 自己。
        分类用 categories 项目代码，读取指定分类用 context --project 项目代码 --category 分类代码。
        交接正文使用 handoff，接收者读取完整正文后用 ack 回执；不要代替他人确认。
        所有写入给 --actor 和稳定 --key；改任务同时给 --expected-revision。
        代码、大文件继续保留原处，只把路径、摘要、证据登记入库。

        源码和完整示例：'''+str(studio/'docs/TEAMHUB.md')+'\n'
                guide=cleandoc(guide)+'\n'
                writes={'teamdb.py':wrapper,'AGENT-GUIDE.md':guide,'README.md':guide,
                        'client.json':json.dumps({'catalog':str(hub/'catalog.json')},ensure_ascii=False,indent=2),
                        'catalog.json':json.dumps(catalog,ensure_ascii=False,indent=2)}
                for name,content in writes.items():
                    (stage/name).write_text(content,encoding='utf-8')
                    if not (hub/name).resolve().is_relative_to(hub):
                        raise ValueError('Unsafe deployment target')
                if hashlib.sha256(old_cli.read_bytes()).hexdigest()!=expected_cli_sha:
                    raise ValueError('Existing CLI changed during preparation; refusing to overwrite')
                # Prevent stale v1 clients silently adding to the now-archived source.
                for table in tables:
                    for action in ('INSERT','UPDATE','DELETE'):
                        live.execute(f'''CREATE TRIGGER archived_{table}_{action.lower()} BEFORE {action} ON {table}
                            BEGIN SELECT RAISE(ABORT,'TeamHub archived: use catalog and per-project database'); END''')
            # Check every move target remains under the explicitly supplied hub, without overwriting.
            final_projects=(hub/'projects').resolve()
            if not final_projects.is_relative_to(hub) or final_projects.exists(): raise ValueError('Unsafe or existing target')
            project_stage.rename(final_projects)
            # A crash here retains prepared projects/backups; refuse automatic re-import on the next call.
        # Catalog is written last as the activation marker. An interrupted deployment is reconciled, not replayed.
        for name,content in writes.items():
            pending=stage/name
            target=(hub/name).resolve()
            if not target.is_relative_to(hub): raise ValueError('Unsafe deployment target')
            pending.replace(target)
    receipt={'schema_version':1,'started_at':started,'completed_at':datetime.now(timezone.utc).isoformat(),
             'source_backup':saved,'old_source':'frozen by write-denial triggers; readable for audit',
             'before':counts,'projects':partitions,'data_rows_reconciled':True,'catalog':str(hub/'catalog.json')}
    (hub/'partition-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
    return receipt


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hub-dir',required=True);parser.add_argument('--expect-cli-sha',required=True)
    args=parser.parse_args()
    try:
        print(json.dumps(install(args.hub_dir,args.expect_cli_sha),ensure_ascii=True,indent=2))
    except (ValueError,OSError,sqlite3.Error) as error:
        parser.exit(1,str(error)+'\n')
