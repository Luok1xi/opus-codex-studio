import json
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.studio_runtime.contracts import load_config, parse_json, validate_plan
from tools.studio_runtime.store import Store, controller_lock
from tools.studio_runtime.routing import Router
from tools.studio_runtime.context import prompt_for
from tools.studio_runtime.engine import Bridge

ROOT = Path(__file__).resolve().parents[1]


def task(name, dependencies=(), read_only=True):
    return {'id': name, 'instruction': 'Inspect ' + name, 'depends_on': list(dependencies),
            'capabilities': ['research' if read_only else 'write'], 'read_only': read_only}


class FakeProviders:
    def __init__(self):
        self.calls = []
        self.probes = 0
        self.quota = {}
        self.fail_lead_once = False
        self.plan = {'tasks': [task('one')]}
        self.approved = True
        self.entered = 0
        self.peak = 0
        self.pause = .005
        self.lock = threading.Lock()

    def probe(self, agent):
        with self.lock:
            self.probes += 1
        return {'available': True, 'reason': None, 'observed_at': time.time(),
                'windows': [{'remaining_percent': self.quota.get(agent['id'], 80), 'reset_at': time.time() + 3600}]}

    def invoke(self, agent, prompt, *, cwd, read_only, session_id, cancel, timeout):
        with self.lock:
            self.calls.append((agent['id'], prompt, read_only))
            self.entered += 1
            self.peak = max(self.peak, self.entered)
        try:
            if agent['id'] == 'opus' and self.fail_lead_once:
                self.fail_lead_once = False
                return {'status': 'quota', 'text': 'Partial plan findings', 'elapsed_ms': 0}
            if cancel.wait(self.pause):
                return {'status': 'cancelled', 'text': '', 'elapsed_ms': 0}
            if 'Act as lead.' in prompt:
                text = json.dumps(self.plan)
            elif 'Review the actual outputs' in prompt:
                text = json.dumps({'approved': self.approved, 'summary': 'Inspected files', 'repair': 'Fix the result'})
            else:
                text = 'Evidence for the assigned work'
            return {'status': 'succeeded', 'text': text, 'session_id': 'test-session', 'usage': {}, 'elapsed_ms': 5}
        finally:
            with self.lock:
                self.entered -= 1


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix='bridge-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.workspace = self.root / 'workspace'
        self.workspace.mkdir()
        self.store = Store(self.root / 'state')
        self.config = load_config(ROOT / 'bridge.example.json')
        self.fake = FakeProviders()
        self.bridge = Bridge(self.store, self.config, self.fake,
                             lambda *a, **kw: {'status': 'succeeded', 'code': 0, 'stdout': 'verified', 'stderr': ''})

    def job(self, tasks=None, key=None):
        return self.store.submit(self.workspace, 'Research and write a useful report', request_key=key,
                                 plan=validate_plan({'tasks': tasks}, self.config) if tasks else None)

    def test_malformed_config_and_lead_output_fail_explicitly(self):
        for text in ('[]', 'null', 'true', '```', '```json\n{}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_json(text)
        self.assertEqual(parse_json('```json\n{"approved": true}\n```'), {'approved': True})
        config_path = self.root / 'invalid.json'
        for field, value in (('enabled', 'false'), ('quota_group', []), ('reserve_balance', float('nan')),
                             ('reasoning_effort', 'unlimited')):
            config = json.loads((ROOT / 'bridge.example.json').read_text())
            config['agents']['codex'][field] = value
            config_path.write_text(json.dumps(config))
            with self.subTest(field=field), self.assertRaises(ValueError):
                load_config(config_path)

        efficient = load_config(ROOT / 'examples' / 'efficient.bridge.json')
        router = Router(efficient, self.fake)
        self.assertEqual(router.select('worker', ['code']), 'codex-worker')
        self.assertEqual(router.select('lead', ['plan']), 'opus')
        router.reject('codex-worker', 'quota')
        self.assertFalse(router.eligible('codex-lead', ['plan']))

        class MalformedLead(FakeProviders):
            def invoke(self, *args, **kwargs):
                return {'status': 'succeeded', 'text': '[]', 'elapsed_ms': 0}

        self.bridge.providers = MalformedLead()
        job = self.bridge.execute(self.job())
        self.assertEqual(job['status'], 'needs-attention')
        self.assertEqual(job['calls'], 1)

    def test_submission_is_idempotent_and_rejects_key_reuse(self):
        self.assertEqual(self.job(key='request-1')['id'], self.job(key='request-1')['id'])
        with self.assertRaises(ValueError):
            self.store.submit(self.workspace, 'different goal', request_key='request-1')
        self.job([task('a')], key='plan-key')
        with self.assertRaises(ValueError):
            self.job([task('b')], key='plan-key')

    def test_dependency_cycles_and_unknown_agents_rejected(self):
        for plan in ([task('a', ['b']), task('b', ['a'])], [task('a', ['absent'])], [task('x'), task('x')]):
            with self.assertRaises(ValueError):
                validate_plan({'tasks': plan}, self.config)
        invalid = task('one') | {'agent': 'unregistered'}
        with self.assertRaises(ValueError):
            validate_plan({'tasks': [invalid]}, self.config)
        with self.assertRaises(ValueError):
            validate_plan({'tasks': [task('one') | {'capabilities': ['unknown_superpower']}]}, self.config)

    def test_plan_cannot_inject_runtime_state_or_native_sessions(self):
        authored = task('one') | {'state': 'succeeded', 'attempt': 3, 'sessions': {'codex': 'private-session'}}
        clean = validate_plan({'tasks': [authored]}, self.config)[0]
        self.assertNotIn('state', clean)
        self.assertNotIn('sessions', clean)
        self.assertNotIn('attempt', clean)

    def test_disabled_agent_cannot_borrow_shared_quota_readiness(self):
        self.config['agents']['disabled'] = dict(self.config['agents']['opus'], enabled=False)
        router = Router(self.config, self.fake)
        router.health('opus')
        self.assertFalse(router.eligible('disabled', []))
        self.assertFalse(router.health('disabled')['available'])

    def test_owner_specialist_route_beats_model_preference_and_keeps_quota_guard(self):
        self.config['routing_rules'] = [
            {'role': 'worker', 'capabilities': ['research'], 'order': ['opus', 'codex']},
            {'role': 'lead', 'capabilities': ['review'], 'order': ['codex', 'opus']}]
        router = Router(self.config, self.fake)
        self.assertEqual(router.select('worker', ['research'], preferred='codex'), 'opus')
        self.assertEqual(router.select('lead', ['review'], preferred='opus'), 'codex')
        self.assertEqual(router.select('lead', ['plan']), 'opus')
        router.reject('opus', 'quota')
        self.assertEqual(router.select('worker', ['research']), 'codex')
        self.assertIsNone(router.select('worker', ['research'], busy=['codex']))

    def test_routing_rules_reject_invalid_candidates_and_role(self):
        path = self.root / 'routing.json'
        good = {'role': 'worker', 'capabilities': ['research'], 'order': ['codex']}
        for bad in (None, [good | {'role': 'boss'}], [good | {'order': ['missing']}],
                    [good | {'capabilities': []}], [good | {'capabilities': ['unknown']}],
                    [good | {'order': [42]}]):
            path.write_text(json.dumps(self.config | {'routing_rules': bad}))
            with self.subTest(rule=bad), self.assertRaises(ValueError):
                load_config(path)

    def test_planning_and_review_have_separate_native_sessions(self):
        sessions = []
        base = self.fake.invoke
        def invoke(*args, **kwargs):
            sessions.append(kwargs.get('session_id'))
            return base(*args, **kwargs)
        self.fake.invoke = invoke
        result = self.bridge.execute(self.job())
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(sessions, [None, None, None])
        self.assertIn('plan:opus', result['role_sessions'])
        self.assertIn('review:opus', result['role_sessions'])

    def test_full_plan_work_review_and_no_model_calls_for_status(self):
        job = self.job()
        result = self.bridge.execute(job)
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(result['calls'], 3)
        self.store.list()
        self.store.events(job['id'])
        self.assertEqual(len(self.fake.calls), 3)
        self.assertTrue(any(x['kind'] == 'plan-accepted' for x in self.store.events(job['id'])))

    def test_opus_quota_fallback_keeps_progress(self):
        self.fake.fail_lead_once = True
        result = self.bridge.execute(self.job())
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(result['lead'], 'codex')
        self.assertEqual(len(self.fake.calls), 4)
        self.assertIn('Partial plan findings', self.fake.calls[1][1])
        self.assertEqual([call[0] for call in self.fake.calls], ['opus', 'codex', 'codex', 'codex'])

    def test_parallel_reads_and_exclusive_writes(self):
        self.fake.pause = .03
        result = self.bridge.execute(self.job([task('a'), task('b'), task('c', ['a', 'b'], False)]))
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(self.fake.peak, 2)
        self.assertEqual(result['metrics']['max_parallel_observed'], 2)
        self.fake.peak = 0
        self.bridge.execute(self.job([task('writer1', read_only=False), task('writer2', read_only=False)]))
        self.assertEqual(self.fake.peak, 1)

    def test_completed_tasks_not_replayed_on_wait_resume(self):
        job = self.job([task('one'), task('two', ['one'])])
        job['tasks'][0]['state'] = 'succeeded'
        result = self.bridge.execute(job)
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(len(self.fake.calls), 2)
        self.assertNotIn('Inspect one', self.fake.calls[0][1])

    def test_crash_recovery_does_not_replay_an_active_writer(self):
        job = self.job([task('writer', read_only=False)])
        job['status'] = 'running'
        job['tasks'][0].update(state='running', attempt=1)
        self.store.save(job)
        self.bridge.run()
        self.assertEqual(self.store.get(job['id'])['status'], 'needs-reconciliation')
        self.assertEqual(self.fake.calls, [])

    def test_process_lock_excludes_second_controller(self):
        with controller_lock(self.store.root):
            with self.assertRaises(RuntimeError):
                with controller_lock(self.store.root):
                    self.fail('Second controller entered')

    def test_failed_checks_override_ai_approval_and_repair_is_bounded(self):
        self.config['checks'] = {'check': ['irrelevant']}
        self.bridge.check_runner = lambda *a, **kw: {'status': 'failed', 'code': 1, 'stdout': '', 'stderr': 'failure'}
        result = self.bridge.execute(self.job())
        self.assertEqual(result['status'], 'needs-attention')
        self.assertEqual(result['repairs'], 1)
        self.assertEqual(result['calls'], 4)
        self.assertIn('Evidence for the assigned work', self.fake.calls[3][1])

    def test_budget_blocks_further_model_calls(self):
        self.config['limits']['max_calls'] = 1
        result = self.bridge.execute(self.job())
        self.assertEqual(result['status'], 'needs-attention')
        self.assertEqual(result['calls'], 1)

    def test_budget_exhaustion_collects_already_running_results(self):
        self.config['limits']['max_calls'] = 1
        result = self.bridge.execute(self.job([task('a'), task('b')]))
        self.assertEqual(result['status'], 'needs-attention')
        self.assertEqual(result['tasks'][0]['state'], 'succeeded')
        self.assertEqual(result['results']['a']['status'], 'succeeded')
        self.assertEqual(result['tasks'][1]['state'], 'pending')

    def test_cancel_reaches_running_workers(self):
        self.fake.pause = 2
        timer = threading.Timer(.04, self.bridge.cancel.set)
        timer.start()
        result = self.bridge.execute(self.job([task('one'), task('two')]))
        timer.join()
        self.assertEqual(result['status'], 'cancelled')
        self.assertEqual(self.fake.entered, 0)

    def test_unknown_exhausted_stale_and_currency_quota(self):
        router = self.bridge.router
        self.fake.quota = {'opus': 0, 'codex': 0}
        self.assertIsNone(router.select('lead'))
        group = router.groups['opus']
        router.cache[group] = {'available': True, 'observed_at': time.time(), 'windows': []}
        self.assertFalse(router.eligible('opus', []))
        router.cache[group] = {'available': True, 'observed_at': time.time(), 'windows': [],
                                   'balance': {'remaining': 5, 'currency': 'USD'}}
        self.assertTrue(router.eligible('opus', []))
        router.cache[group]['balance']['remaining'] = 0
        self.assertFalse(router.eligible('opus', []))

    def test_parallel_quota_queries_coalesce(self):
        router = self.bridge.router
        with ThreadPoolExecutor(max_workers=10) as pool:
            list(pool.map(lambda _: router.health('opus'), range(40)))
        self.assertEqual(self.fake.probes, 1)
        self.assertEqual(router.stats['cache_hits'], 39)

    def test_context_only_contains_dependency_outputs(self):
        job = self.job()
        job['results'] = {str(i): {'status': 'succeeded', 'artifact': {'summary': 'x' * 5000, 'path': f'/{i}'}} for i in range(20)}
        prompt = prompt_for(job, 'Inspect dependency 3', 16000, ['3'])
        self.assertLess(len(prompt), 7000)
        self.assertIn('/3', prompt)
        self.assertNotIn('/19', prompt)
        with self.assertRaises(ValueError):
            prompt_for(job, 'x' * 20000, 16000, [])

    def test_wait_without_capacity_has_zero_inference(self):
        self.fake.quota = {'opus': 0, 'codex': 0}
        result = self.bridge.execute(self.job())
        self.assertEqual(result['status'], 'waiting')
        self.assertEqual(self.fake.calls, [])


if __name__ == '__main__':
    unittest.main()
