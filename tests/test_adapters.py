import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from tools.studio_runtime.adapters import Providers, _run, _window, run_command


FIXTURE = r'''
import json, os, subprocess, sys, time
from pathlib import Path
mode = sys.argv[1]
args = sys.argv[2:]
def emit(data):
    print(json.dumps(data), flush=True)
if 'mcp' in args and 'list' in args:
    if mode == 'mcp_invalid':
        emit({'not': 'a catalog'})
    else:
        disabled = 'mcp_servers.fixture-server.enabled=false' in args
        emit([{'name': 'fixture-server', 'enabled': disabled is False or mode == 'mcp_stuck'}])
    sys.exit(0)
if mode == 'codex_probe':
    for line in sys.stdin:
        data = json.loads(line)
        if data.get('id') == 1:
            emit({'id': 1, 'result': {}})
        elif data.get('id') == 2:
            emit({'id': 2, 'result': {'account': {'email': 'must-not-leak@example.test'}}})
        elif data.get('id') == 3:
            emit({'id': 3, 'result': {'rateLimitsByLimitId': {
                'codex': {'primary': {'usedPercent': 34, 'resetsAt': 2000000000},
                          'secondary': {'usedPercent': 80, 'resetsAt': 2000000100}},
                'review': {'primary': {'usedPercent': 100}}}}})
elif mode == 'claude_auth':
    emit({'loggedIn': False, 'email': 'must-not-leak@example.test'})
    sys.exit(1)
elif mode == 'claude':
    prompt = sys.stdin.read()
    emit({'type': 'result', 'subtype': 'success', 'is_error': False,
          'session_id': '11111111-1111-4111-8111-111111111111',
          'result': json.dumps({'args': args, 'prompt': prompt}), 'usage': {'output_tokens': 4}})
elif mode == 'codex':
    prompt = sys.stdin.read()
    emit({'type': 'thread.started', 'thread_id': '11111111-1111-4111-8111-111111111111'})
    emit({'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'I will inspect the project.'}})
    emit({'type': 'item.completed', 'item': {'type': 'agent_message',
          'text': json.dumps({'args': args, 'prompt': prompt})}})
    emit({'type': 'turn.completed', 'usage': {'input_tokens': 4}})
elif mode == 'quota':
    sys.stdin.read()
    emit({'type': 'turn.failed', 'error': {'message': 'You have hit your usage limit'}})
    sys.exit(1)
elif mode == 'rate':
    sys.stdin.read()
    emit({'type': 'turn.failed', 'error': {'message': '429 rate limit retry later'}})
    sys.exit(1)
elif mode == 'nonzero':
    sys.stdin.read()
    emit({'type': 'turn.completed'})
    sys.exit(2)
elif mode == 'missing':
    sys.stdin.read()
    emit({'type': 'thread.started', 'thread_id': '11111111-1111-4111-8111-111111111111'})
elif mode == 'empty_final':
    sys.stdin.read()
    emit({'type': 'turn.completed', 'usage': {'input_tokens': 4}})
elif mode == 'claude_empty':
    sys.stdin.read()
    emit({'type': 'result', 'subtype': 'success', 'is_error': False, 'result': '   '})
elif mode == 'output':
    print('x' * (5 * 1024 * 1024), flush=True)
elif mode == 'wait':
    time.sleep(20)
elif mode == 'heldpipe':
    import msvcrt
    emit({'pipe': msvcrt.get_osfhandle(sys.stdout.fileno())})
    time.sleep(20)
elif mode in ('tree', 'orphan'):
    child = subprocess.Popen([sys.executable, '-c',
        "from pathlib import Path; import time; time.sleep(1.5); Path('child-finished').write_text('bad')"])
    Path('child-started').write_text(str(child.pid))
    if mode == 'tree':
        time.sleep(20)
elif mode == 'command':
    data = json.load(sys.stdin)
    emit({'status': 'succeeded', 'text': json.dumps(data), 'session_id': 'custom-12', 'usage': {'tokens': 5}})
elif mode == 'command_nonzero':
    sys.stdin.read()
    emit({'status': 'succeeded', 'text': 'not really'})
    sys.exit(1)
elif mode == 'command_probe':
    emit({'available': True, 'windows': [{'remaining_percent': 40, 'reset_at': 2000000000}],
          'observed_at': time.time()})
elif mode == 'command_stale':
    emit({'available': True, 'windows': [{'remaining_percent': 40, 'reset_at': None}],
          'observed_at': 123})
elif mode == 'command_undated':
    emit({'available': True, 'windows': [{'remaining_percent': 100, 'reset_at': None}]})
elif mode == 'command_malformed':
    emit({'available': True, 'windows': [{'remaining_percent': float('nan')},
          {'remaining_percent': float('inf')}, {'remaining_percent': -1},
          {'remaining_percent': 101}, {'remaining_percent': True}], 'observed_at': time.time()})
elif mode == 'command_balance':
    data = json.loads(args[0])
    if data.get('observed_at') == 'now':
        data['observed_at'] = time.time()
    emit(data)
elif mode == 'echo':
    print(sys.stdin.read())
'''


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.cli = self.root / "fixture.py"
        self.cli.write_text(FIXTURE, encoding="utf-8")
        self.providers = Providers()

    def tearDown(self):
        self.temp.cleanup()

    def command(self, mode):
        return [sys.executable, "-X", "utf8", str(self.cli), mode]

    def agent(self, mode, provider="codex"):
        return {"id": "test", "provider": provider, "command": self.command(mode)}

    def invoke(self, mode, **kwargs):
        return self.providers.invoke(self.agent(mode), "你好", cwd=self.root, **kwargs)

    def test_codex_prompt_stdin_and_permissions_on_resume(self):
        first = self.invoke("codex", read_only=True)
        self.assertEqual(first["status"], "succeeded")
        details = json.loads(first["text"])
        self.assertEqual(details["prompt"], "你好")
        self.assertIn('sandbox_mode="read-only"', details["args"])
        self.assertIn('approval_policy="never"', details["args"])
        self.assertIn('mcp_servers.fixture-server.enabled=false', details["args"])
        self.assertIn('features.apps=false', details["args"])
        self.assertIn('features.plugins=false', details["args"])
        self.assertIn('features.hooks=false', details["args"])
        second = self.invoke("codex", session_id=first["session_id"])
        args = json.loads(second["text"])["args"]
        self.assertEqual(args[:2], ["exec", "resume"])
        self.assertIn('sandbox_mode="workspace-write"', args)
        self.assertEqual(second["usage"], {"input_tokens": 4})

    def test_codex_effort_reaches_native_cli_on_new_and_resumed_tasks(self):
        agent = self.agent('codex') | {'reasoning_effort': 'medium'}
        first = self.providers.invoke(agent, 'small task', cwd=self.root, read_only=True)
        self.assertEqual(first['status'], 'succeeded')
        self.assertIn('model_reasoning_effort="medium"', json.loads(first['text'])['args'])
        agent['reasoning_effort'] = 'high'
        resumed = self.providers.invoke(agent, 'review', cwd=self.root, read_only=True, session_id=first['session_id'])
        self.assertEqual(resumed['status'], 'succeeded')
        self.assertIn('model_reasoning_effort="high"', json.loads(resumed['text'])['args'])
        agent['reasoning_effort'] = '--dangerously-bypass-approvals-and-sandbox'
        self.assertEqual(self.providers.invoke(agent, 'invalid', cwd=self.root)['status'], 'failed')

    def test_claude_headless_readonly_and_model(self):
        agent = {**self.agent("claude", "claude"), "model": "opus"}
        result = self.providers.invoke(agent, "review only", cwd=self.root, read_only=True)
        self.assertEqual(result["status"], "succeeded")
        args = json.loads(result["text"])["args"]
        self.assertIn("plan", args)
        self.assertIn("none", args)
        self.assertIn("opus", args)
        self.assertIn("--strict-mcp-config", args)
        self.assertIn('{"mcpServers":{}}', args)
        self.assertIn("mcp__*", args)

    def test_probe_filters_non_codex_windows_and_account_data(self):
        result = self.providers.probe(self.agent("codex_probe"))
        self.assertTrue(result["available"])
        self.assertEqual([item["remaining_percent"] for item in result["windows"]], [66, 20])
        self.assertNotIn("must-not-leak", json.dumps(result))
        self.assertEqual(result["windows"][1]["reset_at"], 2000000100)

    def test_claude_missing_login_does_not_read_credentials(self):
        with patch.object(Providers, "_claude_windows") as usage:
            result = self.providers.probe(self.agent("claude_auth", "claude"))
        self.assertFalse(result["available"])
        usage.assert_not_called()
        self.assertEqual(result["windows"], [])

    def test_deepseek_unverified_is_explicit(self):
        result = self.providers.probe({"id": "deepseek", "provider": "deepseek"})
        self.assertFalse(result["available"])
        self.assertEqual(result["windows"], [])

    def test_failure_cannot_be_reported_as_success(self):
        for mode in ("nonzero", "missing", "empty_final"):
            with self.subTest(mode=mode):
                self.assertEqual(self.invoke(mode)["status"], "failed")
        self.assertEqual(self.invoke("quota")["status"], "quota")
        self.assertEqual(self.invoke("rate")["status"], "failed")
        transcript = '\n'.join(json.dumps(row) for row in [
            {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'done'}},
            {'type': 'turn.completed'}])
        result = Providers._result('codex', {'status': 'io_error', 'code': 0,
                                            'out': transcript, 'err': 'CLI output pipe failed'})
        self.assertEqual(result['status'], 'failed')

    def test_claude_success_requires_nonempty_final_text(self):
        result = self.providers.invoke(self.agent("claude_empty", "claude"), "inspect", cwd=self.root)
        self.assertEqual(result["status"], "failed")
        self.assertIn("final message", result["text"])

    def test_timeout_cancel_and_output_bounds(self):
        self.assertEqual(self.invoke("wait", timeout=.2)["status"], "timeout")
        event = threading.Event()
        timer = threading.Timer(.15, event.set)
        timer.start()
        try:
            self.assertEqual(self.invoke("wait", cancel=event)["status"], "cancelled")
        finally:
            timer.join()
        result = self.invoke("output")
        self.assertEqual(result["status"], "failed")
        self.assertIn("limit", result["text"])
        self.assertLess(len(result["text"]), 100)

    def test_owned_tree_is_terminated(self):
        for mode in ("tree", "orphan"):
            with self.subTest(mode=mode):
                result = run_command(self.command(mode), cwd=self.root, timeout=.6)
                self.assertTrue((self.root / "child-started").exists())
                self.assertEqual(result["status"], "timeout")
                time.sleep(1.6)
                self.assertFalse((self.root / "child-finished").exists())
                (self.root / "child-started").unlink()

    def test_custom_protocol_and_nonzero(self):
        result = self.providers.invoke(self.agent("command", "command"), "inspect", cwd=self.root,
                                       read_only=True, session_id="custom-old")
        self.assertEqual(result["status"], "succeeded")
        data = json.loads(result["text"])
        self.assertTrue(data["read_only"])
        self.assertEqual(data["session_id"], "custom-old")
        bad = self.providers.invoke(self.agent("command_nonzero", "command"), "inspect", cwd=self.root)
        self.assertEqual(bad["status"], "failed")

    def test_custom_probe_keeps_timestamp_and_rejects_undated_quota(self):
        for mode, expected in (("command_probe", 1), ("command_stale", 1), ("command_undated", 0),
                               ("command_malformed", 0)):
            agent = {**self.agent("command", "command"), "probe_command": self.command(mode)}
            result = self.providers.probe(agent)
            self.assertEqual(len(result["windows"]), expected)
            if mode == "command_stale":
                self.assertEqual(result["observed_at"], 123)

    def test_custom_balance_validation_and_router_integration(self):
        from tools.studio_runtime.routing import Router

        base = {"available": True, "windows": [], "observed_at": "now",
                "balance": {"remaining": 12.5, "currency": "CNY"}}
        cases = [(base, True)]
        cases.append(({**base, "windows": [{"remaining_percent": 90}, {"remaining_percent": -1}]}, False))
        cases.append(({**base, "windows": [{"remaining_percent": 90, "reset_at": float('nan')}]}, False))
        for amount in (True, -1, float("inf"), float("nan"), "12.5"):
            cases.append(({**base, "balance": {"remaining": amount, "currency": "CNY"}}, False))
        for currency in (None, "", "cny", "CN", "CNY extra", 123):
            cases.append(({**base, "balance": {"remaining": 12.5, "currency": currency}}, False))
        for observed in (None, 0, -1, float("inf"), float("nan"), time.time() + 100):
            cases.append(({**base, "observed_at": observed}, False))
        for payload, expected in cases:
            agent = {**self.agent("command", "command"), "capabilities": [], "reserve_balance": 1,
                     "probe_command": self.command("command_balance") + [json.dumps(payload)]}
            router = Router({"agents": {"test": agent},
                             "limits": {"quota_ttl_seconds": 60, "reserve_percent": 5}}, self.providers)
            with self.subTest(payload=payload):
                self.assertEqual(router.eligible("test", []), expected)
                result = router.health("test")
                self.assertEqual("balance" in result, expected)
                if expected:
                    self.assertEqual(result["balance"], base["balance"])
        old = {**base, "observed_at": time.time() - 120}
        agent["probe_command"] = self.command("command_balance") + [json.dumps(old)]
        router = Router({"agents": {"test": agent},
                         "limits": {"quota_ttl_seconds": 60, "reserve_percent": 5}}, self.providers)
        self.assertFalse(router.eligible("test", []))

    def test_mcp_configuration_must_be_verified_before_inference(self):
        for mode in ("mcp_invalid", "mcp_stuck"):
            with self.subTest(mode=mode):
                result = self.invoke(mode)
                self.assertEqual(result["status"], "failed")
                self.assertIn("no model was started", result["text"])

    def test_native_quota_malformed_reset_is_not_an_unbounded_window(self):
        for reset in (float('nan'), float('inf'), -1, True, 'invalid-date'):
            self.assertIsNone(_window(10, reset))
        self.assertEqual(_window(10, None), {'remaining_percent': 90, 'reset_at': None})

    @unittest.skipUnless(os.name == 'nt', 'Windows broker handle regression')
    def test_deadline_survives_external_stdout_handle(self):
        import ctypes
        from ctypes import wintypes

        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        kernel.DuplicateHandle.argtypes = [wintypes.HANDLE, wintypes.HANDLE, wintypes.HANDLE,
                                           ctypes.POINTER(wintypes.HANDLE), wintypes.DWORD,
                                           wintypes.BOOL, wintypes.DWORD]
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        held = []
        result = []

        def receive(process, line):
            handle = wintypes.HANDLE()
            self.assertTrue(kernel.DuplicateHandle(int(process._handle), json.loads(line)['pipe'],
                            kernel.GetCurrentProcess(), ctypes.byref(handle), 0, False, 2))
            held.append(handle)
            return False

        worker = threading.Thread(target=lambda: result.append(_run(
            self.command('heldpipe'), cwd=self.root, timeout=.2, on_line=receive)), daemon=True)
        worker.start()
        try:
            worker.join(timeout=2)
            self.assertFalse(worker.is_alive(), 'pipe close blocked despite the deadline')
            self.assertEqual(result[0]['status'], 'timeout')
            self.assertTrue(held)
        finally:
            for handle in held:
                kernel.CloseHandle(handle)
            worker.join(timeout=5)

    def test_mechanical_command_input_and_cancel_before_spawn(self):
        result = run_command(self.command("echo"), cwd=self.root, input_text="literal $(x); hello")
        self.assertEqual(result["status"], "succeeded")
        self.assertEqual(result["stdout"].strip(), "literal $(x); hello")
        event = threading.Event()
        event.set()
        self.assertEqual(run_command(self.command("tree"), cwd=self.root, cancel=event)["status"], "cancelled")
        self.assertFalse((self.root / "child-started").exists())

    def test_invalid_inputs_fail_without_launch(self):
        self.assertEqual(self.invoke("codex", session_id="--last")["status"], "failed")
        self.assertEqual(run_command("echo untrusted", cwd=self.root)["status"], "failed")
        self.assertEqual(self.invoke("codex", timeout=float("nan"))["status"], "failed")


if __name__ == "__main__":
    unittest.main()
