"""Fault scenarios: inspect real effects, not just an agent's success message."""
import json
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tests.test_bridge import FakeProviders, ROOT, task
from tools.studio_runtime.context import artifact
from tools.studio_runtime.contracts import load_config, validate_plan
from tools.studio_runtime.engine import Bridge
from tools.studio_runtime.store import Store


class ResilienceTests(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory(prefix='studio-resilience-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.store = Store(self.root / 'state')
        self.config = load_config(ROOT / 'bridge.example.json')
        self.fake = FakeProviders()
        self.bridge = Bridge(self.store, self.config, self.fake,
                             lambda *a, **kw: {'status': 'succeeded', 'code': 0, 'stdout': '', 'stderr': ''})

    def job(self, tasks):
        return self.store.submit(self.root, 'Complete the specified local work',
                                 plan=validate_plan({'tasks': tasks}, self.config))

    def test_effect_then_lost_receipt_never_blindly_replays_writer(self):
        marker = self.root / 'committed.txt'

        class LostReceipt(FakeProviders):
            def invoke(inner, agent, prompt, **kwargs):
                if not kwargs['read_only']:
                    with marker.open('a') as stream:
                        stream.write('committed\n')
                    if len(marker.read_text().splitlines()) == 1:
                        return {'status': 'quota', 'text': 'Quota exhausted after an action', 'elapsed_ms': 0}
                return super().invoke(agent, prompt, **kwargs)

        provider = LostReceipt()
        self.bridge.providers = provider
        result = self.bridge.execute(self.job([task('write', read_only=False)]))
        self.assertEqual(marker.read_text().splitlines(), ['committed'])
        self.assertEqual(result['status'], 'needs-reconciliation')
        self.assertEqual(result['calls'], 1)

    def test_readonly_crash_resumes_without_replaying_completed_step(self):
        job = self.job([task('done'), task('pending', ['done'])])
        job.update(status='running', calls=2)
        job['tasks'][0]['state'] = 'succeeded'
        job['tasks'][1].update(state='running', attempt=2)
        self.store.save(job)
        self.bridge.run()
        result = self.store.get(job['id'])
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(result['calls'], 4)
        self.assertEqual(len(self.fake.calls), 2)
        self.assertNotIn('Inspect done', self.fake.calls[0][1])

    def test_saved_writer_receipt_survives_crash_before_task_checkpoint(self):
        job = self.job([task('write', read_only=False)])
        job.update(status='running', calls=1)
        job['tasks'][0].update(state='running', attempt=1)
        job['results']['write'] = {'status': 'succeeded', 'attempt': 1, 'agent': 'codex',
                                   'artifact': artifact(self.store.root, 'Actual durable result')}
        self.store.save(job)
        self.bridge.run()
        result = self.store.get(job['id'])
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(len(self.fake.calls), 1)
        self.assertTrue(self.fake.calls[0][2])

    def test_failed_check_with_no_repair_budget_skips_impossible_approval(self):
        self.config['checks'] = {'verify': [sys.executable, '-c', 'raise SystemExit(1)']}
        self.config['limits']['max_repairs'] = 0
        self.bridge.check_runner = lambda *a, **kw: {'status': 'failed', 'code': 1, 'stdout': '', 'stderr': 'wrong output'}
        result = self.bridge.execute(self.job([task('read')]))
        self.assertEqual(result['status'], 'needs-attention')
        self.assertEqual(result['calls'], 1)

    def test_readonly_repair_does_not_gain_write_permissions(self):
        self.fake.approved = False
        result = self.bridge.execute(self.job([task('read')]))
        self.assertEqual(result['status'], 'needs-attention')
        self.assertTrue(all(read_only for _, _, read_only in self.fake.calls))

    def test_uncertain_writer_stops_independent_pending_work(self):
        class FailedWriter(FakeProviders):
            def invoke(inner, agent, prompt, **kwargs):
                inner.calls.append(prompt)
                return {'status': 'timeout', 'text': 'May have written', 'elapsed_ms': 0}

        provider = FailedWriter()
        self.bridge.providers = provider
        result = self.bridge.execute(self.job([task('first', read_only=False), task('second', read_only=False)]))
        self.assertEqual(result['status'], 'needs-reconciliation')
        self.assertEqual(len(provider.calls), 1)
        self.assertEqual(result['tasks'][1]['state'], 'pending')

    def test_specialist_readonly_repair_preserves_capabilities_and_dependencies(self):
        self.config['agents']['codex']['capabilities'] = ['alpha']
        self.config['agents']['opus']['capabilities'] = ['plan', 'review', 'beta']
        self.fake.approved = False
        result = self.bridge.execute(self.job([
            task('first') | {'capabilities': ['alpha']},
            task('second', ['first']) | {'capabilities': ['beta']}]))
        self.assertEqual(result['status'], 'needs-attention')
        self.assertEqual(len(self.fake.calls), 6)
        self.assertEqual(result['tasks'][1]['depends_on'], ['first'])
        self.assertTrue(all(read_only for _, _, read_only in self.fake.calls))
        self.assertIn('Fix the result', self.fake.calls[3][1])
        self.assertFalse(any(e['kind'] == 'contract-error' for e in self.store.events(result['id'])))

    def test_bad_or_stale_receipt_cannot_confirm_writer(self):
        for mode in ('stale', 'corrupt', 'missing', 'malformed'):
            with self.subTest(mode=mode):
                job = self.job([task(mode, read_only=False)])
                job.update(status='running', calls=2)
                job['tasks'][0].update(state='running', attempt=2)
                evidence = artifact(self.store.root, 'Evidence ' + mode)
                receipt = {'status': 'succeeded', 'attempt': 2, 'artifact': evidence}
                if mode == 'stale':
                    receipt['attempt'] = 1
                elif mode == 'corrupt':
                    Path(evidence['path']).write_text('Changed')
                elif mode == 'missing':
                    Path(evidence['path']).unlink()
                else:
                    receipt['artifact'] = None
                job['results'][mode] = receipt
                self.store.save(job)
                self.bridge.run()
                result = self.store.get(job['id'])
                self.assertEqual(result['status'], 'needs-reconciliation')
                self.assertEqual(result['calls'], 2)
        self.assertEqual(len(self.fake.calls), 0)

    def test_checks_or_recovery_limit_do_not_replay_or_reset_budgets(self):
        for phase, recoveries in (('checks', 0), ('work', 2)):
            with self.subTest(phase=phase):
                job = self.job([task('read')])
                job.update(status='running', phase=phase, calls=4, repairs=1, recoveries=recoveries)
                job['tasks'][0].update(state='succeeded' if phase == 'checks' else 'running', attempt=4)
                self.store.save(job)
                self.bridge.run()
                result = self.store.get(job['id'])
                self.assertEqual(result['status'], 'interrupted')
                self.assertEqual((result['calls'], result['repairs'], result['recoveries']), (4, 1, recoveries))
        self.assertEqual(len(self.fake.calls), 0)

    def test_real_process_crash_before_and_after_receipt(self):
        script = '''
import os, sys
from pathlib import Path
from tools.studio_runtime.store import Store
from tools.studio_runtime.context import artifact
store = Store(sys.argv[1])
job = store.get(sys.argv[2])
with Path(job['workspace'], sys.argv[3] + '.txt').open('a') as stream:
    stream.write('committed\\n')
if sys.argv[3] == 'after':
    job['results']['write'] = {'status': 'succeeded', 'attempt': 1,
        'artifact': artifact(store.root, 'Result saved before process crash')}
    store.save(job, 'attempt-finished')
os._exit(17)
'''
        for when in ('before', 'after'):
            with self.subTest(when=when):
                job = self.job([task('write', read_only=False)])
                job.update(status='running', calls=1)
                job['tasks'][0].update(state='running', attempt=1)
                self.store.save(job)
                process = subprocess.run([sys.executable, '-c', script, str(self.store.root), job['id'], when],
                                         cwd=ROOT, capture_output=True, timeout=15)
                self.assertEqual(process.returncode, 17, process.stderr)
                self.bridge.run()
                result = self.store.get(job['id'])
                self.assertEqual(result['status'], 'succeeded' if when == 'after' else 'needs-reconciliation')
                self.assertEqual((self.root / (when + '.txt')).read_text().splitlines(), ['committed'])
        self.assertEqual(len(self.fake.calls), 1)

    def test_readonly_quota_failure_still_hands_off(self):
        class ReadQuota(FakeProviders):
            def invoke(inner, agent, prompt, **kwargs):
                if agent['id'] == 'codex':
                    return {'status': 'quota', 'text': 'Partial read findings', 'elapsed_ms': 0}
                return super().invoke(agent, prompt, **kwargs)

        self.bridge.providers = ReadQuota()
        result = self.bridge.execute(self.job([task('read')]))
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(result['calls'], 3)


if __name__ == '__main__':
    unittest.main()
