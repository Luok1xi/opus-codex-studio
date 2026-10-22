import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from tools.deepseek_task import receipt

ROOT = Path(__file__).resolve().parents[1]


class DeepSeekTaskTests(unittest.TestCase):
    def output(self, *events, status='succeeded', code=0):
        return {'status': status, 'code': code, 'stdout': '\n'.join(json.dumps(x) for x in events), 'stderr': ''}

    def test_only_committed_answer_is_returned(self):
        run = self.output({'type': 'session', 'sessionId': 'session-test'},
                          {'type': 'thinking', 'text': 'private internal reasoning'},
                          {'type': 'status', 'phase': 'turn_end', 'reason': {'kind': 'completed'}},
                          {'type': 'final', 'text': '你好'})
        self.assertEqual(receipt(run), {'status': 'succeeded', 'session_id': 'session-test', 'text': '你好'})

    def test_final_text_alone_cannot_claim_success(self):
        final = {'type': 'final', 'text': 'looks good'}
        for reason in (None, {}, {'kind': 'error'}):
            with self.subTest(reason=reason):
                self.assertEqual(receipt(self.output({'type': 'status', 'phase': 'turn_end', 'reason': reason}, final))['status'], 'failed')
        self.assertEqual(receipt(self.output(final, status='timeout', code=None))['status'], 'timeout')
        self.assertEqual(receipt(self.output(final, code=1))['status'], 'failed')

    def test_error_or_empty_final_is_not_success(self):
        done = {'type': 'status', 'phase': 'turn_end', 'reason': {'kind': 'completed'}}
        for events in ((done, {'type': 'final', 'text': ' '}),
                       (done, {'type': 'error', 'message': 'failed'}, {'type': 'final', 'text': 'partial'})):
            self.assertEqual(receipt(self.output(*events))['status'], 'failed')

    def test_cli_passes_unicode_stdin_and_exact_session_to_owned_process(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            fixture = root / 'fixture.py'
            fixture.write_text('''import json,sys
value = {'prompt': sys.stdin.buffer.read().decode('utf-8'), 'args': sys.argv[1:]}
print(json.dumps({'type':'status','phase':'turn_end','reason':{'kind':'completed'}}))
print(json.dumps({'type':'final','text':json.dumps(value)}))
''', encoding='utf-8')
            connection = root / 'connection.json'
            connection.write_text(json.dumps({'command': [sys.executable, str(fixture)], 'workspace': str(root)}))
            prompt = root / 'prompt.txt'
            prompt.write_text('请打招呼。literal $(noop)', encoding='utf-8')
            run = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'tools/deepseek_task.py'),
                                  '--connection', str(connection), '--prompt-file', str(prompt), '--session', 'session-test'],
                                 capture_output=True, encoding='utf-8', timeout=20)
            self.assertEqual(run.returncode, 0, run.stderr)
            result = json.loads(json.loads(run.stdout)['text'])
            self.assertEqual(result['prompt'], prompt.read_text('utf-8'))
            self.assertEqual(result['args'], ['headless', '--json', '--session-id', 'session-test', '-'])


if __name__ == '__main__':
    unittest.main()
