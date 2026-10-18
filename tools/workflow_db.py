"""Store workflow evidence in its own TeamHub project; never dispatch models."""
import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
import uuid

if __package__:
    from .studio_runtime.teamhub import TeamHub, initialize, now, resolve_database
    from .workflow_review import analyse, nonnegative
else:
    from studio_runtime.teamhub import TeamHub, initialize, now, resolve_database
    from workflow_review import analyse, nonnegative

PROJECT = 'WORKFLOW-STUDIO'
CATEGORIES = [('01','成员工作报告'),('02','效率分析与轮次复盘'),('03','改进建议与状态历史'),
              ('04','验证证据'),('05','归档与协作回执')]
AGENTS = ('codex','opus','dsh')


def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)


def create_project(catalog_path):
    catalog_path=Path(catalog_path).resolve(strict=True)
    lock=catalog_path.with_suffix('.lock')
    # Cooperative registry lock. A stale lock after a crash needs inspection, not blind removal.
    with lock.open('x',encoding='utf-8') as stream:
        stream.write(now())
    try:
        original=catalog_path.read_bytes(); catalog=json.loads(original)
        if catalog.get('schema_version')!=1 or not isinstance(catalog.get('projects'),list):
            raise ValueError('Unsupported project catalog')
        found=[p for p in catalog['projects'] if p['code']==PROJECT]
        if found:
            if len(found)!=1 or found[0]['database']!=f'projects/{PROJECT}/teamhub.db':
                raise ValueError('Conflicting workflow project registration')
            path=(catalog_path.parent/found[0]['database']).resolve(strict=True)
            if not path.is_relative_to(catalog_path.parent): raise ValueError('Unsafe workflow database path')
            hub=TeamHub(path)
            if [p['code'] for p in hub.projects()]!=[PROJECT]: raise ValueError('Mixed project database')
            if [(c['code'],c['name']) for c in hub.categories(PROJECT)]!=CATEGORIES:
                raise ValueError('Incomplete workflow project categories')
            return {'database':str(path),'created':False}
        folder=(catalog_path.parent/'projects'/PROJECT).resolve()
        if not folder.is_relative_to(catalog_path.parent): raise ValueError('Unsafe workflow project path')
        folder.mkdir()  # Never overwrite an orphaned or existing project directory.
        path=folder/'teamhub.db'; initialize(path)
        with closing(sqlite3.connect(path)) as db,db:
            db.execute('INSERT INTO projects(id,code,name,category,status,created_at,updated_at) VALUES(1,?,?,?,?,?,?)',
                       (PROJECT,'工作流研究与改进','workflow','active',now(),now()))
            db.executemany('INSERT INTO project_categories(project_id,code,name) VALUES(1,?,?)',CATEGORIES)
            db.executemany('INSERT INTO agents(code,name,role) VALUES(?,?,?)',
                           [('codex','Codex','实现、验证、集成'),('opus','Opus','设计、独立评审'),('dsh','DeepSeek','采集、分类、证据整理')])
        TeamHub(path).migrate(catalog_path.parent/'backups'/('workflow-init-'+uuid.uuid4().hex+'.db'))
        with closing(sqlite3.connect(path)) as db,db:
            db.execute('CREATE INDEX workflow_report_lookup ON reviews(project_id,target,id)')
            db.execute('CREATE INDEX workflow_decision_lookup ON decisions(project_id,title,id)')
        catalog['projects'].append({'code':PROJECT,'name':'工作流研究与改进','database':f'projects/{PROJECT}/teamhub.db'})
        staged=catalog_path.with_name('catalog.workflow-'+uuid.uuid4().hex+'.json')
        staged.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        if catalog_path.read_bytes()!=original: raise ValueError('Catalog changed; reconcile prepared workflow database')
        staged.replace(catalog_path)
        return {'database':str(path),'created':True}
    finally:
        lock.unlink()


def record(hub, data, *, author, submitted_by, kind, source_project, provenance, evidence=None):
    if author not in AGENTS or submitted_by not in AGENTS:
        raise ValueError('Explicit supported author and submitting agent required')
    if kind not in ('work','analysis'): raise ValueError('kind must be work or analysis')
    if not isinstance(data,dict) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}-[a-z0-9][a-z0-9-]*',str(data.get('round_id',''))):
        raise ValueError('Valid round_id required')
    if not isinstance(source_project,str) or not re.fullmatch('[A-Z0-9][A-Z0-9_-]{0,63}',source_project):
        raise ValueError('Explicit source project code required')
    if not isinstance(provenance,str) or not provenance.strip(): raise ValueError('Authorship/evidence provenance required')
    if evidence is not None and not isinstance(evidence,dict): raise ValueError('Evidence must be a JSON object')
    if kind=='analysis':
        analysis=analyse(data); quality=data['quality']['status']; changes=data['recommendations']
    else:
        if not isinstance(data.get('summary'),str) or not data['summary'].strip(): raise ValueError('Work summary required')
        for field in ('completed','remaining','evidence'):
            if not isinstance(data.get(field),list): raise ValueError('Work report requires '+field)
        if not data['evidence']: raise ValueError('Work evidence required')
        metrics=data.get('metrics',[])
        if not isinstance(metrics,list): raise ValueError('metrics must be a list')
        for metric in metrics:
            if not isinstance(metric,dict) or not all(metric.get(k) for k in ('name','unit','basis')) or 'value' not in metric:
                raise ValueError('Invalid metric')
            if metric['value'] is not None and not nonnegative(metric['value']): raise ValueError('Invalid metric value')
        analysis=None; quality='reported'; changes=[]
    if len({c['id'] for c in changes})!=len(changes): raise ValueError('Duplicate improvement IDs in report')
    payload={'author':author,'kind':kind,'source_project':source_project,'provenance':provenance,
             'report':data,'analysis':analysis,'evidence_payload':evidence}
    digest=hashlib.sha256(canonical(payload).encode('utf-8')).hexdigest()
    key='workflow-report:'+digest+':'+submitted_by

    def write(db,pid):
        previous=None; version=1
        for row in db.execute('SELECT id,notes FROM reviews WHERE project_id=? AND target=? ORDER BY id DESC',(pid,data['round_id'])):
            try: old=json.loads(row['notes'])
            except (ValueError,TypeError): continue
            if not isinstance(old,dict): continue
            if old.get('record_type')!='workflow_report' or old.get('author')!=author or old.get('kind')!=kind: continue
            if old.get('sha256')==digest: return {'project':PROJECT,'table':'reviews','id':row['id'],'duplicate':True,'version':old['version']}
            if previous is None: previous=row['id'];version=old['version']+1
        envelope={'record_type':'workflow_report','schema_version':1,**payload,'submitted_by':submitted_by,
                  'version':version,'previous_review_id':previous,'sha256':digest,
                  'verification':'Reported evidence; peer acceptance requires a separate real review/receipt.'}
        report_id=db.execute('INSERT INTO reviews(project_id,target,reviewer,result,notes,date) VALUES(?,?,?,?,?,?)',
                             (pid,data['round_id'],submitted_by,quality,canonical(envelope),now())).lastrowid
        hub._classify(db,pid,'reviews',report_id,'01' if kind=='work' else '02')
        if evidence is not None: hub._classify(db,pid,'reviews',report_id,'04')
        for change in changes:
            prior=db.execute('SELECT id,status FROM decisions WHERE project_id=? AND title=? ORDER BY id DESC LIMIT 1',(pid,change['id'])).fetchone()
            rationale={'round_id':data['round_id'],'report_id':report_id,'author':author,'owner':change['owner'],
                       'previous_decision_id':prior['id'] if prior else None,'previous_reported_status':prior['status'] if prior else None,
                       'next_check':change['next_check'],'evidence':data['evidence'],'verification':'author-reported status, not automatic approval'}
            did=db.execute('INSERT INTO decisions(project_id,title,decision,rationale,decided_by,decided_at,status) VALUES(?,?,?,?,?,?,?)',
                           (pid,change['id'],change['action'],canonical(rationale),submitted_by,now(),change['status'])).lastrowid
            hub._classify(db,pid,'decisions',did,'03')
        return {'project':PROJECT,'table':'reviews','id':report_id,'duplicate':False,'version':version,'recommendations':len(changes)}
    return hub._write(PROJECT,submitted_by,key,'workflow-report',payload,write)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    init=sub.add_parser('init');init.add_argument('--catalog',required=True)
    save=sub.add_parser('record');save.add_argument('report',type=Path)
    save.add_argument('--author',required=True,choices=AGENTS);save.add_argument('--submitted-by',required=True,choices=AGENTS)
    save.add_argument('--kind',required=True,choices=('work','analysis'));save.add_argument('--source-project',required=True)
    save.add_argument('--provenance',required=True);save.add_argument('--evidence',type=Path)
    save.add_argument('--config');save.add_argument('--db')
    args=parser.parse_args()
    try:
        if args.command=='init': result=create_project(args.catalog)
        else:
            result=record(TeamHub(resolve_database(args.db,args.config,PROJECT)),json.loads(args.report.read_text('utf-8-sig')),
                          author=args.author,submitted_by=args.submitted_by,kind=args.kind,source_project=args.source_project,
                          provenance=args.provenance,evidence=json.loads(args.evidence.read_text('utf-8-sig')) if args.evidence else None)
        print(json.dumps(result,ensure_ascii=False));return 0
    except (ValueError,KeyError,TypeError,OSError,sqlite3.Error) as error:
        print(json.dumps({'error':str(error)},ensure_ascii=False),file=sys.stderr);return 1


if __name__=='__main__':
    if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8');sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
