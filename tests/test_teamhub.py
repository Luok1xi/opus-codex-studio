from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from tools.studio_runtime.teamhub import TeamHub, initialize, resolve_database


class TeamHubTests(unittest.TestCase):
    def setUp(self):
        self.temp=TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name); self.path=self.root/'hub.db'
        initialize(self.path)
        with closing(sqlite3.connect(self.path)) as db:
            db.executemany('INSERT INTO projects(id,code,name) VALUES(?,?,?)',[(1,'A','Project A'),(2,'B','Project B')])
            db.executemany('INSERT INTO project_categories(project_id,code,name) VALUES(?,?,?)',[(1,'01','Algorithms'),(2,'01','Hardware')])
            # Preserve existing data, including incomplete v1 evidence and duplicate resources.
            db.execute("INSERT INTO findings(project_id,topic,claim) VALUES(1,'legacy','unverified')")
            db.execute("INSERT INTO params(project_id,category,item,value) VALUES(1,'01','legacy parameter','2')")
            db.executemany('INSERT INTO resources(project_id,url) VALUES(1,?)',[('https://example.com/',)]*2)
            db.commit()
        self.hub=TeamHub(self.path)
        self.hub.migrate(self.root/'backups/v1.db')

    def test_migration_preserves_rows_backups_and_is_repeatable(self):
        self.assertFalse(self.hub.migrate(self.root/'backups/v1.db')['changed'])
        self.assertEqual(self.hub.query('SELECT count(*) AS n FROM resources')['rows'][0]['n'],2)
        self.assertEqual(self.hub.search('A',category='01')['items'][0]['record']['item'],'legacy parameter')
        self.assertEqual(self.hub.get('A','findings',1)['claim'],'unverified')
        with closing(sqlite3.connect(self.root/'backups/v1.db')) as db:
            self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0],'ok')
            self.assertNotIn('revision',[r[1] for r in db.execute('PRAGMA table_info(tasks)')])
        with self.assertRaises(FileExistsError): self.hub.backup(self.root/'backups/v1.db')
        with self.assertRaises(FileExistsError): initialize(self.path)

    def test_failed_backup_keeps_live_schema_unchanged(self):
        other=self.root/'other.db'; initialize(other)
        with self.assertRaises(FileExistsError): TeamHub(other).migrate(self.path)
        with closing(sqlite3.connect(other)) as db:
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0],0)
            self.assertNotIn('revision',[r[1] for r in db.execute('PRAGMA table_info(tasks)')])

    def test_sql_read_guard_and_query_budget(self):
        for sql in ["WITH x AS (SELECT 1) DELETE FROM projects RETURNING *", 'PRAGMA user_version=99',
                    "ATTACH DATABASE ':memory:' AS leak", 'CREATE TABLE bad(x)',
                    "SELECT load_extension('x')", 'SELECT 1; DELETE FROM projects;']:
            with self.subTest(sql=sql), self.assertRaises(sqlite3.Error): self.hub.query(sql)
        with self.assertRaises(sqlite3.Error):
            self.hub.query('WITH RECURSIVE n(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM n) SELECT sum(x) FROM n')
        self.assertEqual(len(self.hub.query('SELECT * FROM projects',limit=1)['rows']),1)
        self.assertTrue(self.hub.query('SELECT * FROM projects',limit=1)['truncated'])

    def test_project_category_and_full_context_boundaries(self):
        receipt=self.hub.add('findings','A',{'topic':'中文控制','claim':'长文'*9000,'evidence':'measured in fixture','source_ref':'fixture://1'},'codex','finding-1','01')
        self.assertEqual(self.hub.get('A','findings',receipt['id'])['claim'],'长文'*9000)
        with self.assertRaises(ValueError): self.hub.get('B','findings',receipt['id'])
        self.assertEqual(self.hub.search('B',category='01')['items'],[])
        with self.assertRaises(ValueError): self.hub.search('A',category='99')
        brief=self.hub.context('A','01')
        self.assertLessEqual(len(json.dumps(brief,ensure_ascii=False)),12000)
        self.assertTrue(any('claim' in x.get('truncated_fields',[]) for x in brief['items']))
        self.assertGreater(brief['unclassified_counts']['findings'],0)
        with self.assertRaises(ValueError): self.hub.add('findings','A',{'topic':'x','claim':'unsupported'},'codex','bad')

    def test_atomic_resource_dedup_and_idempotency(self):
        def write(i): return self.hub.add('resources','A',{'url':'https://NEW.EXAMPLE/path?a=1'},'dsh',f'r-{i}')
        with ThreadPoolExecutor(max_workers=4) as workers: result=list(workers.map(write,range(8)))
        self.assertEqual(len({r['id'] for r in result}),1)
        self.assertEqual(sum(not r['duplicate'] for r in result),1)
        self.assertTrue(write(0)['duplicate'])
        with self.assertRaises(ValueError): self.hub.add('resources','A',{'url':'https://new.example/different'},'dsh','r-0')
        self.assertNotEqual(self.hub.add('resources','A',{'url':'https://new.example/path?a=2'},'dsh','r-new')['id'],result[0]['id'])

    def test_task_compare_and_swap_and_old_writer_block(self):
        task=self.hub.add('tasks','A',{'title':'review','owner':'codex'},'opus','task-1')
        def update(actor):
            try: return self.hub.update_task('A',task['id'],'in_progress',1,actor,'start-'+actor)
            except ValueError: return None
        with ThreadPoolExecutor(max_workers=2) as workers: results=list(workers.map(update,['codex','opus']))
        self.assertEqual(sum(x is not None for x in results),1)
        self.assertEqual(self.hub.get('A','tasks',task['id'])['revision'],2)
        with closing(sqlite3.connect(self.path)) as legacy:
            with self.assertRaises(sqlite3.IntegrityError): legacy.execute("UPDATE tasks SET status='done' WHERE id=?",(task['id'],))
        with self.assertRaises(ValueError): self.hub.update_task('B',task['id'],'done',2,'codex','wrong-project')

    def test_handoff_recipient_revision_and_repeat_ack(self):
        msg=self.hub.add('handoffs','A',{'marker':'REVIEW-1','to_agent':'opus','body':'完整中文交接'},'codex','send-1','01')
        self.assertEqual(self.hub.inbox('A','opus')[0]['body'],'完整中文交接')
        self.assertEqual(self.hub.inbox('A','codex'),[])
        with self.assertRaises(ValueError): self.hub.ack('A',msg['id'],1,'codex','wrong-recipient')
        first=self.hub.ack('A',msg['id'],1,'opus','ack-1','read')
        self.assertEqual(first,self.hub.ack('A',msg['id'],1,'opus','ack-1','read'))
        self.assertEqual(self.hub.inbox('A','opus'),[])
        self.assertEqual(first['revision'],2)

    def test_export_and_missing_configuration(self):
        exported=self.hub.export(self.root/'export')
        self.assertEqual(exported['manifest']['tables']['projects']['rows'],2)
        self.assertTrue((self.root/'export/manifest.json').is_file())
        with self.assertRaises(FileExistsError): self.hub.export(self.root/'export')
        with self.assertRaises(FileNotFoundError): TeamHub(self.root/'missing.db')
        self.assertFalse((self.root/'missing.db').exists())
        self.assertEqual(resolve_database(self.path),self.path)


if __name__=='__main__': unittest.main()
