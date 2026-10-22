"""Bounded, local CLI adapters. No credentials are copied into studio state."""
from __future__ import annotations

from datetime import datetime
import json
import math
import os
from pathlib import Path
import queue
import re
import shutil
import signal
import subprocess
import threading
import time
import urllib.request
import uuid


OUTPUT_LIMIT = 4 * 1024 * 1024
PROMPT_LIMIT = 1024 * 1024


def _windows_job(process):
    """Own the full descendant tree, including children outliving their parent."""
    import ctypes
    from ctypes import wintypes

    class Basic(ctypes.Structure):
        _fields_ = [("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                    ("flags", wintypes.DWORD), ("min_working", ctypes.c_size_t),
                    ("max_working", ctypes.c_size_t), ("active", wintypes.DWORD),
                    ("affinity", ctypes.c_size_t), ("priority", wintypes.DWORD),
                    ("scheduling", wintypes.DWORD)]

    class Limits(ctypes.Structure):
        _fields_ = [("basic", Basic), ("io", ctypes.c_ulonglong * 6),
                    ("process_memory", ctypes.c_size_t), ("job_memory", ctypes.c_size_t),
                    ("peak_process", ctypes.c_size_t), ("peak_job", ctypes.c_size_t)]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    kernel.CreateJobObjectW.restype = wintypes.HANDLE
    kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.CreateJobObjectW(None, None)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())
    limits = Limits()
    limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    try:
        if not kernel.SetInformationJobObject(handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            raise ctypes.WinError(ctypes.get_last_error())
        if not kernel.AssignProcessToJobObject(handle, int(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())
        native = ctypes.WinDLL("ntdll")
        native.NtResumeProcess.argtypes = [wintypes.HANDLE]
        native.NtResumeProcess.restype = ctypes.c_long
        if native.NtResumeProcess(int(process._handle)) != 0:
            raise OSError("Could not resume owned worker")
    except BaseException:
        kernel.CloseHandle(handle)
        raise
    return lambda: kernel.CloseHandle(handle)


def _command(agent):
    command = agent.get("command")
    if command is not None:
        if not isinstance(command, list) or not command or not all(
                isinstance(part, str) and part and "\0" not in part for part in command):
            raise ValueError("command must be a nonempty argument list")
        return command.copy()
    name = {"codex": "codex", "claude": "claude"}.get(agent.get("provider"))
    if not name:
        return None
    found = shutil.which(name)
    if found:
        return [found]
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData/Local")))
        roaming = Path(os.environ.get("APPDATA", str(Path.home() / "AppData/Roaming")))
        paths = (base / "OpenAI/Codex/bin").glob("*/codex.exe") if name == "codex" else (
            roaming / "Claude/claude-code").glob("*/*/claude.exe")
        candidates = sorted(paths, key=lambda path: path.stat().st_mtime, reverse=True)
        if candidates:
            return [str(candidates[0])]
    return None


def _terminate(process):
    # Only a live child owned by this call is ever signalled; never reload PIDs.
    if os.name == "nt":
        if process.poll() is not None:
            return
        try:
            subprocess.run(["taskkill.exe", "/PID", str(process.pid), "/T", "/F"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
        except (OSError, subprocess.TimeoutExpired):
            process.kill()
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def _cancel_pipe_io(workers):
    if os.name != "nt":
        return
    import ctypes
    from ctypes import wintypes

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenThread.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenThread.restype = wintypes.HANDLE
    kernel.CancelSynchronousIo.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    for worker in workers:
        if worker.is_alive() and worker.native_id is not None:
            handle = kernel.OpenThread(1, False, worker.native_id)  # THREAD_TERMINATE access, not termination.
            if handle:
                kernel.CancelSynchronousIo(handle)
                kernel.CloseHandle(handle)


def _run(command, *, cwd=None, stdin="", timeout=20, cancel=None, on_line=None):
    """Drain both pipes without unbounded communicate() buffers or shell parsing."""
    if cancel is not None and cancel.is_set():
        return {"status": "cancelled", "code": None, "out": "", "err": ""}
    process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               creationflags=(subprocess.CREATE_NO_WINDOW | 0x4) if os.name == "nt" else 0,
                               start_new_session=os.name != "nt")
    close_job = None
    if os.name == "nt":
        try:
            close_job = _windows_job(process)
        except BaseException:
            process.kill()
            process.wait(timeout=5)
            for pipe in (process.stdin, process.stdout, process.stderr):
                pipe.close()
            raise
    messages = queue.Queue(maxsize=16)
    stopped = threading.Event()

    def offer(item):
        while not stopped.is_set():
            try:
                messages.put(item, timeout=.1)
                return
            except queue.Full:
                pass

    def drain(pipe, name):
        try:
            while not stopped.is_set() and (block := pipe.read1(65536)):
                offer((name, block))
        except (OSError, ValueError):
            if not stopped.is_set():
                offer(("io_error", b"CLI output pipe failed"))
        finally:
            pipe.close()
            offer((name, None))

    def write_input():
        try:
            process.stdin.write(stdin.encode("utf-8"))
            process.stdin.flush()
            if on_line is None:
                process.stdin.close()
        except (OSError, ValueError):
            pass

    workers = [threading.Thread(target=drain, args=(process.stdout, "out"), daemon=True),
               threading.Thread(target=drain, args=(process.stderr, "err"), daemon=True),
               threading.Thread(target=write_input, daemon=True)]
    for worker in workers:
        worker.start()
    buffers = {"out": bytearray(), "err": bytearray()}
    ended, total, pending = 0, 0, b""
    deadline = time.monotonic() + timeout
    status = "exited"
    try:
        while ended < 2:
            if cancel is not None and cancel.is_set():
                status = "cancelled"
                break
            if time.monotonic() >= deadline:
                status = "timeout"
                break
            try:
                name, block = messages.get(timeout=.05)
            except queue.Empty:
                continue
            if name == "io_error":
                status = "io_error"
                buffers["err"].extend(block)
                break
            if block is None:
                ended += 1
                continue
            total += len(block)
            if total > OUTPUT_LIMIT:
                status = "output_limit"
                break
            buffers[name].extend(block)
            if name == "out" and on_line:
                pending += block
                while b"\n" in pending:
                    line, pending = pending.split(b"\n", 1)
                    if on_line(process, line.decode("utf-8", errors="replace")):
                        status = "resolved"
                        break
                if status == "resolved":
                    break
        if status == "exited":
            try:
                process.wait(timeout=max(.01, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                status = "timeout"
    finally:
        stopped.set()
        if close_job:
            close_job()
        _terminate(process)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        _cancel_pipe_io(workers)
        for worker, pipe in zip(workers, (process.stdout, process.stderr, process.stdin)):
            worker.join(timeout=.2)
            # A broker may retain a pipe outside our Job; never wait on another thread's buffer lock.
            if not worker.is_alive():
                try:
                    if pipe is process.stdin and not pipe.closed:
                        pipe.raw.close()  # Cancelled input must not be flushed again during close.
                    pipe.close()
                except (OSError, ValueError):
                    pass
        if any(worker.is_alive() for worker in workers):
            buffers["err"].extend(b"\nStudio: pipe cleanup remains pending outside the owned process tree.")
    return {"status": status, "code": process.returncode,
            **{key: bytes(value).decode("utf-8", errors="replace") for key, value in buffers.items()}}


def run_command(command, *, cwd, cancel=None, timeout=600, input_text=""):
    """Execute an explicitly authorized mechanical check, without a shell."""
    try:
        command = _command({"command": command})
        if not _number(timeout) or not 0 < timeout <= 86400:
            raise ValueError("Invalid command timeout")
        if not isinstance(input_text, str) or len(input_text.encode("utf-8")) > PROMPT_LIMIT:
            raise ValueError("Command input exceeds 1 MiB")
        run = _run(command, cwd=cwd, stdin=input_text, timeout=timeout, cancel=cancel)
        state = run["status"]
        status = state if state in ("cancelled", "timeout") else (
            "succeeded" if state == "exited" and run["code"] == 0 else "failed")
        return {"status": status, "code": run["code"], "stdout": run["out"],
                "stderr": "Output limit exceeded" if state == "output_limit" else run["err"]}
    except (OSError, ValueError, TypeError, subprocess.SubprocessError) as exc:
        return {"status": "failed", "code": None, "stdout": "", "stderr": _public_error(str(exc))}


def _json(line):
    try:
        value = json.loads(line)
        return value if isinstance(value, dict) else {}
    except (ValueError, TypeError):
        return {}


def _number(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value)


def _window(used, reset):
    if not _number(used) or not 0 <= used <= 100:
        return None
    if isinstance(reset, str):
        try:
            reset = datetime.fromisoformat(reset.replace("Z", "+00:00")).timestamp()
        except ValueError:
            return None
    if reset is not None and (not _number(reset) or reset <= 0):
        return None
    return {"remaining_percent": 100 - used, "reset_at": reset}


def _public_error(text):
    text = re.sub(r"(?i)Bearer\s+\S+", "Bearer [redacted]", str(text))
    text = re.sub(r"\bsk-[a-zA-Z0-9_-]+", "[redacted]", text)
    return text[:2000]


def _usage(value):
    return {key: number for key, number in value.items()
            if isinstance(key, str) and len(key) <= 64 and _number(number)
            and number >= 0} if isinstance(value, dict) else {}


def _session(value):
    try:
        return str(uuid.UUID(value)) if isinstance(value, str) else None
    except ValueError:
        return None


def _codex_isolation(command, cwd, cancel, deadline):
    # Empty TOML tables merge with user settings; disable each effective server explicitly.
    flags = ["-c", "features.apps=false", "-c", "features.plugins=false",
             "-c", "features.hooks=false", "-c", "features.skill_mcp_dependency_install=false"]
    for verify in (False, True):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("MCP isolation deadline exceeded")
        run = _run(command + flags + ["mcp", "list", "--json"], cwd=cwd,
                   timeout=min(10, remaining), cancel=cancel)
        if run["status"] == "cancelled":
            raise InterruptedError("Task cancelled during MCP isolation")
        if run["status"] == "timeout":
            raise TimeoutError("MCP isolation deadline exceeded")
        if run["status"] != "exited" or run["code"] != 0:
            raise ValueError("Could not verify Codex MCP isolation; no model was started")
        try:
            servers = json.loads(run["out"])
        except ValueError:
            servers = None
        if not isinstance(servers, list) or not all(isinstance(item, dict) for item in servers):
            raise ValueError("Invalid Codex MCP catalog; no model was started")
        for item in servers:
            name = item.get("name")
            if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,256}", name):
                raise ValueError("Invalid Codex MCP server identity")
            if verify:
                if item.get("enabled") is not False:
                    raise ValueError("Codex MCP server remained enabled; no model was started")
            else:
                flags += ["-c", f"mcp_servers.{name}.enabled=false"]
    return flags


def _failure(text):
    value = text.lower()
    if any(word in value for word in ("usage limit", "quota_exceeded", "insufficient_quota",
                                      "credit balance", "hit your limit", "quota exhausted")):
        return "quota"
    if any(word in value for word in ("not logged in", "authentication", "unauthorized",
                                      "invalid api key", "login required", "please log in")):
        return "auth"
    return "failed"


class Providers:
    def probe(self, agent):
        result = {"available": False, "reason": None, "observed_at": time.time(), "windows": []}
        provider = agent.get("provider")
        if provider == "deepseek":
            result["reason"] = "DeepSeek headless CLI contract is not configured or verified"
            return result
        try:
            command = _command(agent)
            if not command:
                result["reason"] = "Official CLI not found"
            elif provider == "codex":
                self._probe_codex(command, result)
            elif provider == "claude":
                run = _run(command + ["auth", "status", "--json"])
                auth = _json(run["out"])
                result["available"] = auth.get("loggedIn") is True
                result["reason"] = "Quota unknown" if result["available"] else "Claude CLI login required"
                if result["available"]:
                    result["windows"] = self._claude_windows(agent.get("model"))
                    if result["windows"]:
                        result["reason"] = None
            elif provider == "command":
                if not agent.get("probe_command"):
                    result.update(available=True, reason="Custom command readiness and quota unknown")
                else:
                    probe = _run(_command({"command": agent["probe_command"]}))
                    data = _json(probe["out"])
                    if probe["status"] == "exited" and probe["code"] == 0 and isinstance(data.get("available"), bool):
                        result["available"] = data["available"]
                        result["reason"] = _public_error(data.get("reason") or "") or None
                        windows = data.get("windows", [])
                        invalid_window = not isinstance(windows, list)
                        for item in windows if isinstance(windows, list) else []:
                            window = None
                            if isinstance(item, dict) and _number(item.get("remaining_percent")):
                                reset = item.get("reset_at")
                                if reset is None or (_number(reset) and reset > 0):
                                    window = _window(100 - item["remaining_percent"], reset)
                            if window is None:
                                invalid_window = True
                            else:
                                result["windows"].append(window)
                        if invalid_window:
                            result.update(available=False, windows=[], reason="Custom quota contains an invalid window")
                            return result
                        observed = data.get("observed_at")
                        # The custom bridge must supply evidence time; a static reply cannot become fresh.
                        if not _number(observed) or observed <= 0 or observed > time.time():
                            result["windows"] = []
                            result["reason"] = "Custom quota has no valid observation time"
                        else:
                            result["observed_at"] = observed
                            balance = data.get("balance")
                            if isinstance(balance, dict):
                                amount, currency = balance.get("remaining"), balance.get("currency")
                                if (_number(amount) and amount >= 0 and isinstance(currency, str)
                                        and re.fullmatch(r"[A-Z]{3}", currency)):
                                    result["balance"] = {"remaining": amount, "currency": currency}
                                else:
                                    result["reason"] = "Custom balance has invalid amount or currency"
                        return result
                    result["reason"] = "Custom command probe failed or returned invalid JSON"
            else:
                result["reason"] = "Unsupported provider"
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            result["reason"] = f"CLI probe unavailable ({type(exc).__name__})"
        result["observed_at"] = time.time()
        return result

    @staticmethod
    def _probe_codex(command, result):
        def send(process, message):
            process.stdin.write((json.dumps(message) + "\n").encode("utf-8"))
            process.stdin.flush()

        def receive(process, line):
            message = _json(line)
            if message.get("id") == 1:
                if message.get("error"):
                    result["reason"] = "Codex app-server initialization failed"
                    return True
                send(process, {"method": "initialized", "params": {}})
                send(process, {"id": 2, "method": "account/read", "params": {"refreshToken": False}})
            elif message.get("id") == 2:
                data = message.get("result")
                if message.get("error") or not isinstance(data, dict) or not data.get("account"):
                    result["reason"] = "Codex CLI login required or account unavailable"
                    return True
                result["available"] = True
                send(process, {"id": 3, "method": "account/rateLimits/read", "params": {}})
            elif message.get("id") == 3:
                data = message.get("result")
                data = data if isinstance(data, dict) else {}
                by_id = data.get("rateLimitsByLimitId")
                # Other products (for example review) do not describe Codex task capacity.
                limits = by_id.get("codex", {}) if isinstance(by_id, dict) else data.get("rateLimits", {})
                invalid_window = False
                for key in ("primary", "secondary"):
                    item = limits.get(key) if isinstance(limits, dict) else None
                    if isinstance(item, dict):
                        window = _window(item.get("usedPercent"), item.get("resetsAt"))
                        if window is not None:
                            result["windows"].append(window)
                        else:
                            invalid_window = True
                    elif item is not None:
                        invalid_window = True
                if invalid_window:
                    result.update(windows=[], reason="Codex quota contains an invalid window")
                else:
                    result["reason"] = None if result["windows"] else "Quota unknown"
                return True
            return False

        initial = {"id": 1, "method": "initialize", "params": {
            "clientInfo": {"name": "studio_bridge", "version": "1.0.0"}}}
        run = _run(command + ["app-server", "--listen", "stdio://"],
                   stdin=json.dumps(initial) + "\n", on_line=receive)
        if run["status"] != "resolved":
            result["reason"] = "Quota unknown" if result["available"] else "Codex account probe unavailable"

    @staticmethod
    def _claude_windows(model=None):
        # Read only the official CLI's credential source; never persist or return its contents.
        directory = Path(os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude")))
        try:
            with (directory / ".credentials.json").open("rb") as handle:
                raw = handle.read(65537)
            if len(raw) > 65536:
                return []
            oauth = _json(raw).get("claudeAiOauth", {})
            if not isinstance(oauth, dict):
                return []
            token = oauth.get("accessToken")
            if not isinstance(token, str) or not token or "\n" in token:
                return []
            request = urllib.request.Request("https://api.anthropic.com/api/oauth/usage", headers={
                "Authorization": "Bearer " + token, "anthropic-beta": "oauth-2025-04-20"})
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None

            with urllib.request.build_opener(NoRedirect()).open(request, timeout=8) as response:
                data = _json(response.read(65536))
            keys = ["five_hour", "seven_day"]
            for family in ("opus", "sonnet"):
                if isinstance(model, str) and family in model.lower():
                    keys.append("seven_day_" + family)
            windows = []
            for key in keys:
                item = data.get(key)
                if item is None:
                    continue
                if not isinstance(item, dict):
                    return []
                window = _window(item.get("utilization"), item.get("resets_at"))
                if window is None:
                    return []
                windows.append(window)
            return windows
        except (OSError, ValueError, TypeError):
            return []

    def invoke(self, agent, prompt, *, cwd, read_only=False, session_id=None, cancel=None, timeout=600):
        started = time.monotonic()
        result = {"status": "failed", "text": "", "session_id": None, "usage": {}, "elapsed_ms": 0}
        try:
            if not isinstance(prompt, str) or not prompt or len(prompt.encode("utf-8")) > PROMPT_LIMIT:
                raise ValueError("prompt must be nonempty and at most 1 MiB")
            if not _number(timeout) or not 0 < timeout <= 86400:
                raise ValueError("timeout must be between 0 and 86400 seconds")
            directory = Path(cwd).resolve(strict=True)
            if not directory.is_dir():
                raise ValueError("cwd must be a directory")
            provider = agent.get("provider")
            if session_id is not None:
                if provider != "command":
                    session_id = str(uuid.UUID(session_id))
                elif not isinstance(session_id, str) or not 0 < len(session_id) <= 256:
                    raise ValueError("Invalid custom session identifier")
            if provider not in ("codex", "claude", "command"):
                raise ValueError("Provider has no verified headless adapter")
            command = _command(agent)
            if not command:
                raise ValueError("Official CLI not found")
            model = agent.get("model")
            if model is not None and (not isinstance(model, str) or not model or model.startswith("-")):
                raise ValueError("Invalid model name")
            if provider == "codex":
                isolation = _codex_isolation(command, str(directory), cancel, started + timeout)
                sandbox = "read-only" if read_only else "workspace-write"
                command += ["exec"] + (["resume"] if session_id else [])
                command += ["--skip-git-repo-check", "--json", "-c", 'approval_policy="never"',
                            "-c", f'sandbox_mode="{sandbox}"']
                command += isolation
                if model:
                    command += ["--model", model]
                if "reasoning_effort" in agent:
                    effort = agent["reasoning_effort"]
                    if effort not in ("low", "medium", "high", "xhigh", "max"):
                        raise ValueError("Invalid reasoning effort")
                    command += ["-c", 'model_reasoning_effort=' + json.dumps(effort)]
                command += ([session_id] if session_id else []) + ["-"]
            elif provider == "claude":
                command += ["-p", "--output-format", "stream-json", "--verbose",
                            "--permission-mode", "plan" if read_only else "acceptEdits",
                            "--permission-prompts", "none", "--strict-mcp-config",
                            "--mcp-config", '{"mcpServers":{}}', "--disallowedTools", "mcp__*"]
                if model:
                    command += ["--model", model]
                if session_id:
                    command += ["--resume", session_id]
            else:
                prompt = json.dumps({"prompt": prompt, "cwd": str(directory),
                                     "read_only": read_only, "session_id": session_id})
            remaining = started + timeout - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Task deadline exceeded")
            run = _run(command, cwd=str(directory), stdin=prompt, cancel=cancel, timeout=remaining)
            result.update(self._result(provider, run))
        except TimeoutError:
            result.update(status="timeout", text="Task deadline exceeded")
        except InterruptedError:
            result.update(status="cancelled", text="Task cancelled")
        except (OSError, ValueError, TypeError, subprocess.SubprocessError) as exc:
            result["text"] = _public_error(str(exc))
        result["elapsed_ms"] = round((time.monotonic() - started) * 1000)
        return result

    @staticmethod
    def _result(provider, run):
        result = {"status": "failed", "text": "", "session_id": None, "usage": {}}
        if provider == "command" and run["status"] == "exited":
            data = _json(run["out"])
            allowed = ("succeeded", "quota", "auth", "failed", "cancelled", "timeout")
            if data.get("status") not in allowed or not isinstance(data.get("text"), str):
                result["text"] = "Custom command returned an invalid result"
                return result
            result.update(status=data["status"], text=data["text"],
                          usage=_usage(data.get("usage")))
            session = data.get("session_id")
            if isinstance(session, str) and 0 < len(session) <= 256:
                result["session_id"] = session
            if run["code"] != 0 and result["status"] == "succeeded":
                result.update(status="failed", text="Custom command exited nonzero after reporting success")
            return result
        complete, messages, errors = False, [], []
        for line in run["out"].splitlines():
            event = _json(line)
            kind = event.get("type")
            if kind == "thread.started":
                result["session_id"] = _session(event.get("thread_id"))
            if event.get("session_id"):
                result["session_id"] = _session(event["session_id"])
            if provider == "codex":
                item = event.get("item")
                item = item if isinstance(item, dict) else {}
                if kind == "item.completed" and item.get("type") == "agent_message":
                    if isinstance(item.get("text"), str) and item["text"].strip():
                        messages.append(item["text"])
                if kind == "turn.completed":
                    complete = True
                    result["usage"] = _usage(event.get("usage"))
                if kind in ("error", "turn.failed"):
                    errors.append(str(event.get("message") or event.get("error") or "Codex task failed"))
            elif kind == "result":
                complete = event.get("is_error") is False and event.get("subtype") == "success"
                result["usage"] = _usage(event.get("usage"))
                if complete:
                    if isinstance(event.get("result"), str) and event["result"].strip():
                        messages.append(event["result"])
                else:
                    errors.append(str(event.get("errors") or event.get("result") or event.get("subtype")))
        if run["status"] in ("cancelled", "timeout"):
            result["status"] = run["status"]
            result["text"] = "Task cancelled" if run["status"] == "cancelled" else "Task deadline exceeded"
        elif run["status"] == "output_limit":
            result["text"] = "CLI output exceeded the 4 MiB limit"
        elif run["status"] == "exited" and run["code"] == 0 and complete and messages and not errors:
            result["status"] = "succeeded"
            result["text"] = messages[-1]
        else:
            error = "\n".join(errors) or run["err"] or "CLI exited without a successful final message"
            result["status"] = _failure(error)
            result["text"] = _public_error(error)
        return result
