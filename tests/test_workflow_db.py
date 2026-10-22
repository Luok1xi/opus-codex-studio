from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import copy
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from tools.studio_runtime.teamhub import TeamHub, initialize
from tools.workflow_db import CATEGORIES, PROJECT, create_project, record


def work_report():
    return dict(round_id='2026-10-18-database-test', summary='完整中文工作报告\n' * 100,
                completed=['已完成回读'], remaining=[], evidence=['fixture://receipt'],
                metrics=[dict(name='usage', value=None, unit='tokens', basis='not reported')])


def analysis_report():
    return dict(schema_version=1, round_id='2026-10-18-database-test', task_summary='database test',
                workflow_version='v1', started_at='2026-10-18T00:00:00Z',
                measurement_cutoff_at='2026-10-18T00:01:00Z',
                quality=dict(status='passed', acceptance=['check'], completed=['check'], remaining=[]),
                metrics=[], observations=[], evidence=['fixture://receipt'], comparison=None, limits=['test fixture'],
                recommendations=[dict(id='TEST-IMPROVEMENT-1', action='核对证据', owner='codex',
                                      status='proposed', next_check='下一轮检查实际回执')])


class WorkflowDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        other_folder = self.root / 'projects' / 'OTHER'
        other_folder.mkdir(parents=True)
        self.other = other_folder / 'teamhub.db'
        initialize(self.other)
        with closing(sqlite3.connect(self.other)) as db, db:
            db.execute("INSERT INTO projects(code,name) VALUES('OTHER','Existing project')")
        self.other_before = self.other.read_bytes()
        self.catalog = self.root / 'catalog.json'
        self.original_catalog = dict(schema_version=1, roles={'codex': 'implementation'},
                                     projects=[dict(code='OTHER', name='Existing project',
                                                    database='projects/OTHER/teamhub.db')])
        self.catalog.write_text(json.dumps(self.original_catalog), encoding='utf-8')
        self.created = create_project(self.catalog)
        self.hub = TeamHub(self.created['database'])

    def save(self, data=None, **options):
        arguments = dict(author='opus', submitted_by='codex', kind='work',
                         source_project='OTHER', provenance='Imported from fixture://author-reply')
        arguments.update(options)
        return record(self.hub, work_report() if data is None else data, **arguments)

    def counts(self):
        return {table: self.hub.query('SELECT count(*) AS n FROM ' + table)['rows'][0]['n']
                for table in ('reviews', 'decisions', 'record_categories', 'events', 'write_keys')}

    def envelope(self, receipt):
        return json.loads(self.hub.get(PROJECT, 'reviews', receipt['id'])['notes'])

    def test_initialization_is_repeatable_and_preserves_other_project(self):
        catalog_before = self.catalog.read_bytes()
        database_before = self.hub.path.read_bytes()
        backups_before = list((self.root / 'backups').iterdir())
        repeated = create_project(self.catalog)
        self.assertTrue(self.created['created'])
        self.assertFalse(repeated['created'])
        self.assertEqual(repeated['database'], self.created['database'])
        self.assertEqual(self.catalog.read_bytes(), catalog_before)
        self.assertEqual(self.hub.path.read_bytes(), database_before)
        self.assertEqual(self.other.read_bytes(), self.other_before)
        self.assertEqual(list((self.root / 'backups').iterdir()), backups_before)
        catalog = json.loads(catalog_before)
        self.assertEqual(catalog['projects'][:-1], self.original_catalog['projects'])
        self.assertEqual(catalog['roles'], self.original_catalog['roles'])
        self.assertEqual([p['code'] for p in self.hub.projects()], [PROJECT])
        self.assertEqual([(c['code'], c['name']) for c in self.hub.categories(PROJECT)], CATEGORIES)
        self.assertFalse(self.catalog.with_suffix('.lock').exists())

    def test_author_submitter_and_full_evidence_survive_readback(self):
        data = work_report()
        evidence = {'source': 'fixture://receipt', 'body': '完整证据' * 200}
        receipt = self.save(data, evidence=evidence)
        row = self.hub.get(PROJECT, 'reviews', receipt['id'])
        saved = json.loads(row['notes'])
        self.assertEqual(row['reviewer'], 'codex')
        self.assertEqual(saved['author'], 'opus')
        self.assertEqual(saved['submitted_by'], 'codex')
        self.assertEqual(saved['report'], data)
        self.assertEqual(saved['evidence_payload'], evidence)
        self.assertIsNone(saved['report']['metrics'][0]['value'])
        self.assertEqual(self.hub.search(PROJECT, category='04')['items'][0]['id'], receipt['id'])
        brief = self.hub.context(PROJECT, '01')['items'][0]
        self.assertIn('notes', brief['truncated_fields'])
        self.assertNotEqual(brief['record']['notes'], row['notes'])

    def test_concurrent_identical_requests_create_one_report(self):
        with ThreadPoolExecutor(max_workers=4) as workers:
            receipts = list(workers.map(lambda _: self.save(), range(12)))
        self.assertEqual(len({r['id'] for r in receipts}), 1)
        self.assertEqual(sum(not r['duplicate'] for r in receipts), 1)
        self.assertEqual(self.counts()['reviews'], 1)
        self.assertEqual(self.counts()['write_keys'], 1)
        # A different importing agent must not duplicate the same author's report.
        repeat = self.save(submitted_by='dsh')
        self.assertTrue(repeat['duplicate'])
        self.assertEqual(repeat['id'], receipts[0]['id'])
        self.assertEqual(self.counts()['reviews'], 1)

    def test_revisions_keep_original_report_and_recommendation_history(self):
        original = analysis_report()
        first = self.save(original, kind='analysis')
        updated = copy.deepcopy(original)
        updated['recommendations'][0]['status'] = 'adopted'
        updated['evidence'].append('fixture://implementation')
        second = self.save(updated, kind='analysis')
        self.assertEqual(second['version'], 2)
        self.assertEqual(self.envelope(first)['report'], original)
        self.assertEqual(self.envelope(second)['report'], updated)
        self.assertEqual(self.envelope(second)['previous_review_id'], first['id'])
        self.assertIsNone(self.envelope(second)['analysis']['observed_time_change_pct'])
        rows = self.hub.query('SELECT * FROM decisions ORDER BY id')['rows']
        self.assertEqual([r['status'] for r in rows], ['proposed', 'adopted'])
        rationale = json.loads(rows[1]['rationale'])
        self.assertEqual(rationale['previous_decision_id'], rows[0]['id'])
        self.assertEqual(rationale['previous_reported_status'], 'proposed')
        self.assertEqual(rationale['report_id'], second['id'])
        repeat = self.save(original, kind='analysis')
        self.assertTrue(repeat['duplicate'])
        self.assertEqual(repeat['id'], first['id'])
        self.assertEqual(self.counts()['decisions'], 2)

    def test_author_and_kind_have_separate_version_chains(self):
        opus = self.save()
        codex = self.save(author='codex')
        analysis = self.save(analysis_report(), kind='analysis')
        self.assertEqual(len({opus['id'], codex['id'], analysis['id']}), 3)
        for receipt in (opus, codex, analysis):
            self.assertEqual(receipt['version'], 1)
            self.assertIsNone(self.envelope(receipt)['previous_review_id'])

    def test_failure_rolls_back_all_rows_and_original_request_can_retry(self):
        before = self.counts()
        classify = self.hub._classify

        def fail_after_decision(db, pid, table, entity_id, category):
            classify(db, pid, table, entity_id, category)
            if table == 'decisions':
                raise RuntimeError('Injected failure after report and decision inserts')

        with patch.object(self.hub, '_classify', side_effect=fail_after_decision):
            with self.assertRaisesRegex(RuntimeError, 'Injected failure'):
                self.save(analysis_report(), kind='analysis')
        self.assertEqual(self.counts(), before)
        receipt = self.save(analysis_report(), kind='analysis')
        self.assertFalse(receipt['duplicate'])
        self.assertEqual(receipt['version'], 1)
        after = self.counts()
        self.assertEqual(after['reviews'] - before['reviews'], 1)
        self.assertEqual(after['decisions'] - before['decisions'], 1)
        self.assertEqual(after['record_categories'] - before['record_categories'], 2)
        self.assertEqual(after['events'] - before['events'], 1)
        self.assertEqual(after['write_keys'] - before['write_keys'], 1)

    def test_invalid_reports_and_metadata_leave_database_unchanged(self):
        cases = []
        for field, value in [('round_id', '../bad'), ('summary', ''), ('evidence', []), ('completed', 'bad')]:
            changed = work_report()
            changed[field] = value
            cases.append((changed, {}))
        for value in (float('nan'), float('inf'), -1, True):
            changed = work_report()
            changed['metrics'][0]['value'] = value
            cases.append((changed, {}))
        for options in ({'author': 'unknown'}, {'submitted_by': 'unknown'}, {'kind': 'unknown'},
                        {'source_project': '../OTHER'}, {'provenance': ''}, {'evidence': []}):
            cases.append((work_report(), options))
        changed = analysis_report()
        changed['quality']['remaining'] = ['Unmet acceptance criterion']
        cases.append((changed, {'kind': 'analysis'}))
        changed = analysis_report()
        changed['recommendations'] *= 2
        cases.append((changed, {'kind': 'analysis'}))
        before = self.counts()
        for index, (data, options) in enumerate(cases):
            with self.subTest(case=index), self.assertRaises(ValueError):
                self.save(data, **options)
            self.assertEqual(self.counts(), before)


if __name__ == '__main__':
    unittest.main()
