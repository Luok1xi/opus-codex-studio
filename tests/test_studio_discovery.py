import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from tools.install_codex_skill import install
from tools.studio_runtime.consult import consult
from tools.studio_runtime.store import Store

ROOT = Path(__file__).resolve().parents[1]


class DiscoveryTests(unittest.TestCase):
    def test_install_preserves_existing_guidance_and_is_repeatable(self):
        with TemporaryDirectory() as folder:
            home = Path(folder)
            (home / 'AGENTS.md').write_bytes(b'Keep my conventions.\r\n')
            skill = install(home)
            first = (home / 'AGENTS.md').read_bytes()
            install(home)
            self.assertEqual((home / 'AGENTS.md').read_bytes(), first)
            self.assertEqual((home / 'AGENTS.before-ai-studio.md').read_bytes(), b'Keep my conventions.\r\n')
            self.assertIn(ROOT.as_posix(), skill.read_text('utf-8'))
            self.assertNotIn('@STUDIO_ROOT@', skill.read_text('utf-8'))
            self.assertIn(skill.as_posix(), first.decode('utf-8'))
            (home / 'AGENTS.override.md').write_text('Existing override')
            with self.assertRaises(ValueError):
                install(home)
            self.assertEqual((home / 'AGENTS.md').read_bytes(), first)

    def test_consult_saves_answer_and_never_replays_key(self):
        with TemporaryDirectory() as folder:
            store = Store(Path(folder) / 'state')
            calls = []
            def invoke(*args, **kwargs):
                calls.append(kwargs)
                return {'status': 'succeeded', 'session_id': 'session-example', 'text': 'Useful answer'}
            kwargs = dict(workspace=folder, prompt='Review the proposal', connection='owner.json', key='review-1')
            job = consult(store, invoke, **kwargs)
            self.assertEqual(job['status'], 'answered')
            answer = job['results']['consult']
            self.assertEqual(Path(answer['artifact']['path']).read_text('utf-8'), 'Useful answer')
            self.assertEqual(answer['session_id'], 'session-example')
            self.assertEqual(consult(store, invoke, **kwargs)['id'], job['id'])
            self.assertEqual(len(calls), 1)
            self.assertEqual(store.list(ready=True), [])
            with self.assertRaises(ValueError):
                consult(store, invoke, **(kwargs | {'prompt': 'Different paid work'}))

    def test_consult_failure_and_crash_require_reconciliation(self):
        for failure in ('timeout', 'exception'):
            with self.subTest(failure=failure), TemporaryDirectory() as folder:
                store = Store(Path(folder) / 'state')
                def invoke(*args, **kwargs):
                    if failure == 'exception':
                        raise OSError('Connection lost after possible action')
                    return {'status': 'timeout', 'text': 'Partial'}
                try:
                    consult(store, invoke, workspace=folder, prompt='Work', connection='owner.json', key='one')
                except OSError:
                    pass
                job = store.list()[0]
                self.assertEqual(job['status'], 'needs-reconciliation')
                job['status'] = 'running'  # Simulate death before the final save.
                store.save(job)
                store.recover_interrupted(max_recoveries=2)
                self.assertEqual(store.get(job['id'])['status'], 'needs-reconciliation')
                self.assertEqual(store.list(ready=True), [])

    def test_pending_consult_is_not_a_queued_workflow(self):
        with TemporaryDirectory() as folder:
            store = Store(Path(folder) / 'state')
            store.submit(folder, 'Explicit request', kind='consult')
            self.assertEqual(store.list(ready=True), [])

    def test_shared_cli_uses_existing_headless_and_retains_receipt(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            fixture = root / 'runtime.py'
            fixture.write_text('''import json,sys
print(json.dumps({'type':'session','sessionId':'session-native'}))
print(json.dumps({'type':'status','phase':'turn_end','reason':{'kind':'completed'}}))
print(json.dumps({'type':'final','text':sys.stdin.buffer.read().decode('utf-8')}))
''', encoding='utf-8')
            config = root / 'connection.json'
            config.write_text(json.dumps({'command': [sys.executable, str(fixture)], 'workspace': folder}))
            prompt = root / 'task.txt'
            prompt.write_text('只回复：接入成功', encoding='utf-8')
            command = [sys.executable, '-X', 'utf8', str(ROOT / 'tools/bridge.py'), '--state', str(root / 'state'),
                       'consult', '--connection', str(config), '--workspace', folder, '--prompt-file', str(prompt), '--key', 'same']
            run = subprocess.run(command, cwd=folder, capture_output=True, encoding='utf-8', timeout=20)
            self.assertEqual(run.returncode, 0, run.stderr)
            job = json.loads(run.stdout)
            self.assertEqual(job['status'], 'answered')
            self.assertEqual(job['results']['consult']['session_id'], 'session-native')
            fixture.write_text('raise RuntimeError("Must not run twice")')
            repeated = subprocess.run(command, cwd=folder, capture_output=True, encoding='utf-8', timeout=20)
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertEqual(json.loads(repeated.stdout)['id'], job['id'])
