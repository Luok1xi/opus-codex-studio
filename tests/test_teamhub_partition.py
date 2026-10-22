from contextlib import closing
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import sqlite3
import time
from tempfile import TemporaryDirectory
import unittest

from tools.studio_runtime.teamhub import TeamHub, initialize, resolve_database
from tools import teamhub_partition


class PartitionTests(unittest.TestCase):
    def setUp(self):
        self.temp=TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.path=self.root/'teamhub.db'
        initialize(self.path);(self.root/'teamdb.py').write_text('# original CLI',encoding='utf-8')
        self.sha=hashlib.sha256((self.root/'teamdb.py').read_bytes()).hexdigest()
        with closing(sqlite3.connect(self.path)) as db:
            db.executemany('INSERT INTO projects(id,code,name) VALUES(?,?,?)',[(1,'A','A name'),(2,'B','B name')])
            db.executemany('INSERT INTO sources(project_id,title,url) VALUES(?,?,?)',[(1,'private A','https://a.example/'),(2,'private B','https://b.example/')])
            db.commit()

    def test_split_reconciles_isolates_freezes_and_routes(self):
        receipt=teamhub_partition.install(self.root,self.sha)
        self.assertTrue(receipt['data_rows_reconciled'])
        config=self.root/'client.json'
        a=TeamHub(resolve_database(config=config,project='A'))
        b=TeamHub(resolve_database(config=config,project='B'))
        self.assertNotEqual(a.path,b.path)
        self.assertEqual(a.query('SELECT title FROM sources')['rows'],[{'title':'private A'}])
        self.assertEqual(b.query('SELECT title FROM sources')['rows'],[{'title':'private B'}])
        with closing(sqlite3.connect(self.path)) as old:
            with self.assertRaises(sqlite3.IntegrityError): old.execute("INSERT INTO resources(url) VALUES('https://late.example/')")
            self.assertEqual(old.execute('SELECT count(*) FROM sources').fetchone()[0],2)
        self.assertTrue(Path(receipt['source_backup']['path']).is_file())
        with self.assertRaises(ValueError): teamhub_partition.install(self.root,self.sha)

    def test_changed_source_and_unassigned_data_are_not_overwritten(self):
        with self.assertRaises(ValueError): teamhub_partition.install(self.root,'wrong-hash')
        with closing(sqlite3.connect(self.path)) as db:
            db.execute("INSERT INTO sources(title) VALUES('unassigned')");db.commit()
        with self.assertRaises(ValueError): teamhub_partition.install(self.root,self.sha)
        self.assertFalse((self.root/'catalog.json').exists())
        with closing(sqlite3.connect(self.path)) as db:
            db.execute("INSERT INTO resources(url) VALUES('https://still-writable.example/')");db.commit()

    def test_catalog_rejects_shared_file_and_mixed_project_target(self):
        teamhub_partition.install(self.root,self.sha)
        catalog_path=self.root/'catalog.json'; config=self.root/'client.json'
        catalog=json.loads(catalog_path.read_text('utf-8'))
        original=catalog['projects'][1]['database']
        catalog['projects'][1]['database']=catalog['projects'][0]['database']
        catalog_path.write_text(json.dumps(catalog),encoding='utf-8')
        with self.assertRaises(ValueError): resolve_database(config=config,project='A')
        catalog['projects'][1]['database']=original
        catalog['projects'][0]['database']='teamhub.db'
        catalog_path.write_text(json.dumps(catalog),encoding='utf-8')
        with self.assertRaises(ValueError): resolve_database(config=config,project='A')

    def test_ambiguous_legacy_category_stays_unclassified(self):
        with closing(sqlite3.connect(self.path)) as db,db:
            db.execute("INSERT INTO project_categories(project_id,code,name) VALUES(1,'01','Evidence')")
            db.execute("INSERT INTO project_categories(project_id,code,name) VALUES(1,'02','01')")
            db.execute("UPDATE sources SET category='01' WHERE project_id=1")
        teamhub_partition.install(self.root,self.sha)
        hub=TeamHub(resolve_database(config=self.root/'client.json',project='A'))
        self.assertEqual(hub.query('SELECT count(*) AS n FROM record_categories')['rows'],[{'n':0}])

    def test_inflight_old_writer_is_preserved_then_blocked(self):
        with closing(sqlite3.connect(self.path)) as old:
            old.execute('BEGIN IMMEDIATE')
            old.execute("INSERT INTO sources(project_id,title,url) VALUES(1,'just committed','https://new.example/')")
            with ThreadPoolExecutor(max_workers=1) as pool:
                future=pool.submit(teamhub_partition.install,self.root,self.sha)
                time.sleep(0.1)
                self.assertFalse(future.done())
                old.commit()
                receipt=future.result(timeout=10)
            self.assertEqual(receipt['before']['sources'],3)
            current=TeamHub(resolve_database(config=self.root/'client.json',project='A'))
            self.assertEqual(current.query("SELECT title FROM sources WHERE title='just committed'")['rows'],[{'title':'just committed'}])
            with self.assertRaises(sqlite3.IntegrityError):
                old.execute("INSERT INTO sources(project_id,title) VALUES(1,'late')")


if __name__=='__main__': unittest.main()
