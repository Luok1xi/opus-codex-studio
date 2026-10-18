import json
from contextlib import closing
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from tools.studio_runtime.teamhub import initialize


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'tools/teamdb.py'


class TeamDBCLITests(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory(prefix='teamdb-cli-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.db = self.root / 'shared.db'
        initialize(self.db)
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.executemany('INSERT INTO projects(code,name) VALUES(?,?)',
                             [('ALPHA', 'Alpha project'), ('BETA', 'Beta project')])
            conn.execute("INSERT INTO project_categories(project_id,code,name) SELECT id,'01','Evidence' FROM projects")
        self.cli('migrate', '--backup', str(self.root / 'before-v2.db'))

    def cli(self, *arguments, ok=True, database=None, config=None):
        location = ['--config', str(config)] if config else ['--db', str(database or self.db)]
        result = subprocess.run([sys.executable, '-B', str(CLI), *location, '--json', *arguments],
                                cwd=self.root, capture_output=True, encoding='utf-8', timeout=20,
                                env={key: value for key, value in os.environ.items() if key.upper() != 'TEAMHUB_DB'})
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        error = json.loads(result.stderr)
        self.assertTrue(error['error'])
        return error

    def test_missing_database_fails_without_creating_file(self):
        missing = self.root / 'missing.db'
        self.cli('projects', database=missing, ok=False)
        self.assertFalse(missing.exists())

    def test_explicit_init_migration_backup(self):
        fresh = self.root / 'new.db'
        self.cli('init', database=fresh)
        self.cli('init', database=fresh, ok=False)
        backup = self.root / 'new-v1.db'
        self.cli('migrate', '--backup', str(backup), database=fresh)
        self.assertTrue(backup.is_file())
        before = backup.read_bytes()
        self.cli('migrate', '--backup', str(backup), database=fresh)
        self.assertEqual(backup.read_bytes(), before)

    def test_two_roles_exchange_full_body_and_ack_once(self):
        body = '复核资料正文，不截断。' * 40 + '\n保留此换行与来源。'
        body_file = self.root / 'handoff.txt'
        body_file.write_text(body, encoding='utf-8')
        arguments = ('handoff', '--project', 'ALPHA', '--actor', 'opus', '--to-agent', 'codex',
                     '--marker', 'REVIEW-001', '--body-file', str(body_file), '--key', 'send-1')
        sent = self.cli(*arguments)
        repeated = self.cli(*arguments)
        self.assertEqual(sent['id'], repeated['id'])
        self.assertTrue(repeated['duplicate'])
        record = self.cli('get', '--project', 'ALPHA', 'handoffs', str(sent['id']))
        self.assertEqual(record['body'], body)
        inbox = self.cli('inbox', '--project', 'ALPHA', '--agent', 'codex')
        self.assertEqual(len(inbox), 1)
        self.assertEqual(self.cli('inbox', '--project', 'BETA', '--agent', 'codex'), [])
        self.assertEqual(self.cli('inbox', '--project', 'ALPHA', '--agent', 'opus'), [])
        self.cli('ack', '--project', 'ALPHA', '--id', str(sent['id']), '--revision', str(record['revision']),
                 '--actor', 'opus', '--key', 'bad-ack', ok=False)
        acknowledgement = ('ack', '--project', 'ALPHA', '--id', str(sent['id']),
                           '--expected-revision', str(record['revision']), '--actor', 'codex', '--key', 'ack-1')
        acked = self.cli(*acknowledgement)
        self.assertEqual(acked['status'], 'acked')
        self.assertEqual(self.cli(*acknowledgement)['revision'], acked['revision'])
        self.assertEqual(self.cli('inbox', '--project', 'ALPHA', '--agent', 'codex'), [])
        body_file.write_text('Different work', encoding='utf-8')
        self.cli(*arguments, ok=False)

    def test_explicit_category_mapping_and_project_isolation(self):
        for project, key, mapped in (('ALPHA', 'source-a', True), ('ALPHA', 'source-unmapped', False),
                                     ('BETA', 'source-b', True)):
            arguments = ['add-source', '--project', project, '--title', key,
                         '--url', 'https://example.com/' + key, '--category', 'video', '--by', 'dsh', '--key', key]
            if mapped:
                arguments += ['--category-code', '01']
            self.cli(*arguments)
        categories = self.cli('categories', 'ALPHA')
        self.assertEqual(categories[0]['code'], '01')
        result = self.cli('search', '--project', 'ALPHA', '--category', '01', '--table', 'sources')
        self.assertEqual([item['record']['title'] for item in result['items']], ['source-a'])
        self.assertEqual(result['items'][0]['record']['category'], 'video')
        record_id = result['items'][0]['id']
        self.cli('get', '--project', 'BETA', 'sources', str(record_id), ok=False)
        self.cli('context', '--project', 'ALPHA', '--category', '01')

    def test_readonly_query_and_untruncated_json(self):
        long_name = '完整字段' * 100
        with closing(sqlite3.connect(self.db)) as conn, conn:
            conn.execute("UPDATE projects SET name=? WHERE code='ALPHA'", (long_name,))
        result = self.cli('query', "SELECT name FROM projects WHERE code='ALPHA'")
        self.assertEqual(result['rows'][0]['name'], long_name)
        for sql in ('PRAGMA user_version=7',
                    "WITH x AS (SELECT 1) UPDATE projects SET name='changed' RETURNING id"):
            self.cli('query', sql, ok=False)
        self.assertEqual(self.cli('query', "SELECT name FROM projects WHERE code='ALPHA'")['rows'][0]['name'], long_name)

    def test_task_revision_prevents_stale_update(self):
        added = self.cli('add-task', '--project', 'ALPHA', '--title', 'Review evidence',
                         '--owner', 'codex', '--actor', 'opus', '--key', 'task-1')
        record = self.cli('get', '--project', 'ALPHA', 'tasks', str(added['id']))
        update = ['update-task', '--project', 'ALPHA', '--id', str(added['id']), '--status', 'in_progress',
                  '--expected-revision', str(record['revision']), '--actor', 'codex']
        changed = self.cli(*update, '--key', 'start-1')
        self.assertGreater(changed['revision'], record['revision'])
        self.cli(*update, '--key', 'stale-2', ok=False)
        self.assertEqual(len(self.cli('list-tasks', '--project', 'ALPHA')['items']), 1)

    def test_legacy_add_flags_preserve_evidence_and_actor(self):
        cases = (
            ('add-resource', 'resources', ['--url', 'https://example.com/resource', '--found-in', 'reference'], 'found_by'),
            ('add-finding', 'findings', ['--topic', 'Topic', '--claim', 'Claim', '--evidence', 'Measured', '--ref', 'Source'], None),
            ('add-param', 'params', ['--category', 'speed', '--item', 'Speed', '--value', '4.7', '--unit', 'm/s', '--ref', 'Source'], None),
            ('add-decision', 'decisions', ['--title', 'Decision', '--decision', 'Verify first', '--rationale', 'Need evidence'], 'decided_by'),
            ('add-artifact', 'artifacts', ['--name', 'Report', '--path', 'report.txt', '--type', 'report'], None),
        )
        for command, table, fields, actor_field in cases:
            with self.subTest(command=command):
                added = self.cli(command, '--project', 'ALPHA', '--by', 'dsh', '--key', command, *fields)
                record = self.cli('get', '--project', 'ALPHA', table, str(added['id']))
                if actor_field:
                    self.assertEqual(record[actor_field], 'dsh')
                if table in ('findings', 'params'):
                    self.assertEqual(record['source_ref'], 'Source')

    def test_catalog_routes_two_independent_database_files(self):
        projects = []
        for code in ('ONE', 'TWO'):
            relative = Path('projects') / code / 'teamhub.db'
            database = self.root / relative
            database.parent.mkdir(parents=True)
            initialize(database)
            with closing(sqlite3.connect(database)) as conn, conn:
                conn.execute('INSERT INTO projects(code,name) VALUES(?,?)', (code, code + ' project'))
            self.cli('migrate', '--backup', str(database.with_suffix('.v1.db')), database=database)
            projects.append({'code': code, 'name': code + ' project', 'database': relative.as_posix()})
        catalog = self.root / 'catalog.json'
        catalog.write_text(json.dumps({'schema_version': 1, 'projects': projects}), encoding='utf-8')
        config = self.root / 'catalog-config.json'
        config.write_text(json.dumps({'catalog': str(catalog)}), encoding='utf-8')
        self.assertEqual({row['code'] for row in self.cli('projects', config=config)}, {'ONE', 'TWO'})
        for code in ('ONE', 'TWO'):
            self.cli('add-task', '--project', code, '--title', code + ' task', '--owner', 'codex',
                     '--actor', 'opus', '--key', 'same-key-in-independent-databases', config=config)
            project_rows = self.cli('query', '--project', code, 'SELECT code FROM projects', config=config)
            self.assertEqual(project_rows['rows'], [{'code': code}])
            task_rows = self.cli('query', '--project', code, 'SELECT title FROM tasks', config=config)
            self.assertEqual(task_rows['rows'], [{'title': code + ' task'}])
            statistics = self.cli('stats', '--project', code, config=config)
            self.assertEqual(next(row['count'] for row in statistics if row['table'] == 'projects'), 1)
        self.cli('query', 'SELECT code FROM projects', config=config, ok=False)
        self.cli('query', '--project', 'MISSING', 'SELECT code FROM projects', config=config, ok=False)
        self.cli('init', config=config, ok=False)
        self.assertFalse((self.root / 'teamhub.db').exists())


if __name__ == '__main__':
    unittest.main()
