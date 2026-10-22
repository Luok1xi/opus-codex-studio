import { spawn, execFile } from 'node:child_process';

// Stop only a child owned by this process. Never kill a PID read from an old lock file.
export async function stopChild(child) {
  if (!child.pid || child.exitCode !== null || child.signalCode !== null) return;
  if (process.platform === 'win32') {
    await new Promise(resolve => execFile('taskkill.exe', ['/PID', String(child.pid), '/T', '/F'],
      { windowsHide: true, timeout: 10000 }, () => resolve()));
  } else {
    try { process.kill(-child.pid, 'SIGKILL'); } catch { /* already exited */ }
  }
}

export function runProcess(executable, args, { cwd, input = '', timeoutMs = 600000, signal, env = {}, onLine } = {}) {
  return new Promise(resolve => {
    if (signal?.aborted) return resolve({ code: null, reason: 'cancelled', stdout: '', stderr: '' });
    const child = spawn(executable, args, { cwd, env: { ...process.env, ...env },
      windowsHide: true, detached: process.platform !== 'win32', stdio: ['pipe', 'pipe', 'pipe'] });
    let stdout = '', stderr = '', pending = '', reason = null, settled = false;
    const limit = 2 * 1024 * 1024;
    const finish = code => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      signal?.removeEventListener('abort', abort);
      if (pending) onLine?.(pending);
      resolve({ code, reason, stdout, stderr });
    };
    const stop = why => { if (!reason) { reason = why; void stopChild(child); } };
    const abort = () => stop('cancelled');
    const timer = setTimeout(() => stop('timeout'), timeoutMs);
    signal?.addEventListener('abort', abort, { once: true });
    child.stdout.setEncoding('utf8');
    child.stderr.setEncoding('utf8');
    child.stdout.on('data', chunk => {
      stdout = (stdout + chunk).slice(-limit);
      pending += chunk;
      let end;
      while ((end = pending.indexOf('\n')) >= 0) {
        const line = pending.slice(0, end); pending = pending.slice(end + 1); onLine?.(line);
      }
      if (pending.length > limit) { pending = ''; stop('output-limit'); }
    });
    child.stderr.on('data', chunk => { stderr = (stderr + chunk).slice(-limit); });
    child.on('error', () => { reason = 'launch-failed'; finish(null); });
    child.on('close', finish);
    child.stdin.on('error', () => {});
    child.stdin.end(input);
  });
}
