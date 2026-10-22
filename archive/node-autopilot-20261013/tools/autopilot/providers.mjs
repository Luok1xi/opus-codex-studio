import { spawn, execFileSync } from 'node:child_process';
import { existsSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { createInterface } from 'node:readline';
import { createClaudeLimitReader } from '@backnotprop/orchestrator-core/provider-limits';
import { runProcess, stopChild } from './process.mjs';

function findExecutable(name, roots, depth = 0) {
  try {
    const matches = execFileSync(process.platform === 'win32' ? 'where.exe' : 'which', [name],
      { encoding: 'utf8', windowsHide: true, stdio: ['ignore', 'pipe', 'ignore'] }).trim().split(/\r?\n/);
    if (matches[0] && existsSync(matches[0])) return matches[0];
  } catch { /* bundled clients need not be on PATH */ }
  const found = [];
  function visit(root, level) {
    if (!root || !existsSync(root)) return;
    for (const entry of readdirSync(root, { withFileTypes: true })) {
      const path = join(root, entry.name);
      if (entry.isFile() && entry.name.toLowerCase() === name.toLowerCase()) found.push(path);
      else if (entry.isDirectory() && level > 0) visit(path, level - 1);
    }
  }
  for (const root of roots) visit(root, depth);
  return found.sort((a, b) => statSync(b).mtimeMs - statSync(a).mtimeMs)[0] ?? null;
}

export function discover() {
  const win = process.platform === 'win32';
  return {
    codex: findExecutable(win ? 'codex.exe' : 'codex', [join(process.env.LOCALAPPDATA || '', 'OpenAI/Codex/bin')], 2),
    claude: findExecutable(win ? 'claude.exe' : 'claude', [join(process.env.APPDATA || '', 'Claude/claude-code')], 3),
    deepseek: null,
  };
}

export async function readCodexQuota(executable) {
  const base = { id: 'codex', checkedAt: new Date().toISOString(), source: 'account/rateLimits/read', windows: [] };
  if (!executable) return { ...base, available: false, reason: 'not-installed' };
  const child = spawn(executable, ['app-server', '--listen', 'stdio://'],
    { windowsHide: true, detached: process.platform !== 'win32', stdio: ['pipe', 'pipe', 'ignore'] });
  const lines = createInterface({ input: child.stdout });
  return new Promise(resolve => {
    let done = false;
    const finish = async result => {
      if (done) return;
      done = true; clearTimeout(timer); lines.close(); child.stdin.end();
      await stopChild(child); resolve({ ...base, ...result });
    };
    const send = message => { if (!done) child.stdin.write(JSON.stringify(message) + '\n'); };
    const timer = setTimeout(() => void finish({ available: false, reason: 'quota-timeout' }), 15000);
    child.on('error', () => void finish({ available: false, reason: 'launch-failed' }));
    child.on('exit', () => { if (!done) void finish({ available: false, reason: 'probe-exited' }); });
    child.stdin.on('error', () => {});
    lines.on('line', line => {
      let msg; try { msg = JSON.parse(line); } catch { return; }
      if (msg.id === 1) {
        if (msg.error) return void finish({ available: false, reason: 'initialize-failed' });
        send({ method: 'initialized', params: {} });
        send({ id: 2, method: 'account/rateLimits/read', params: {} });
      }
      if (msg.id !== 2) return;
      if (msg.error) return void finish({ available: false, reason: 'quota-unavailable' });
      const snapshots = msg.result?.rateLimitsByLimitId ?? { codex: msg.result?.rateLimits };
      const quota = snapshots.codex ?? msg.result?.rateLimits;
      const windows = ['primary', 'secondary'].flatMap(key => {
        const value = quota?.[key];
        return Number.isFinite(value?.usedPercent) ? [{ id: key, usedPercent: value.usedPercent,
          resetsAt: value.resetsAt ? new Date(value.resetsAt * 1000).toISOString() : null }] : [];
      });
      void finish({ available: windows.length > 0, reason: windows.length ? null : 'quota-unknown', windows });
    });
    send({ id: 1, method: 'initialize', params: { clientInfo: { name: 'local_studio', version: '1.0.0' } } });
  });
}

export async function doctor(executables = discover()) {
  const [codex, claude] = await Promise.all([
    readCodexQuota(executables.codex),
    (async () => {
      const base = { id: 'claude', checkedAt: new Date().toISOString(), windows: [] };
      if (!executables.claude) return { ...base, available: false, reason: 'not-installed' };
      const auth = await runProcess(executables.claude, ['auth', 'status', '--json'], { timeoutMs: 15000 });
      let status; try { status = JSON.parse(auth.stdout); } catch { return { ...base, available: false, reason: 'auth-unavailable' }; }
      if (!status.loggedIn) return { ...base, available: false, reason: 'login-required' };
      // The library reads the original CLI credential store in memory; no token/account data is persisted here.
      const snapshot = await createClaudeLimitReader({ authStatusCommand: async () => ({ ok: true, status }) })
        .read({ provider: 'claude', workspaceRoot: process.cwd(), timeoutMs: 15000 });
      const windows = snapshot.windows.filter(w => !/sonnet/i.test(w.id + w.label))
        .map(w => ({ id: w.id, usedPercent: w.usedPercent, resetsAt: w.resetsAt ?? null }));
      return { ...base, source: snapshot.source, available: windows.length > 0,
        reason: windows.length ? null : 'quota-unknown', windows };
    })().catch(() => ({ id: 'claude', available: false, windows: [], checkedAt: new Date().toISOString(), reason: 'quota-unavailable' })),
  ]);
  return { checkedAt: new Date().toISOString(), agents: [claude, codex,
    { id: 'deepseek', available: false, reason: 'adapter-not-verified', windows: [], checkedAt: new Date().toISOString() }] };
}

export function selectAgent(report, config, excluded = [], preferred) {
  const order = preferred ? [preferred, ...config.priority.filter(x => x !== preferred)] : config.priority;
  return order.find(id => {
    const row = report.agents.find(a => a.id === id);
    return !excluded.includes(id) && row?.available && Date.now() - Date.parse(row.checkedAt) <= config.quotaMaxAgeMs
      && row.windows.length > 0 && row.windows.every(w => Number.isFinite(w.usedPercent) && w.usedPercent >= 0
        && w.usedPercent <= 100 - config.reservePercent
        && (!w.resetsAt || Date.parse(w.resetsAt) > Date.now()));
  }) ?? null;
}

export function parseJson(text) {
  const clean = text.trim().replace(/^```(?:json)?\s*/, '').replace(/\s*```$/, '');
  return JSON.parse(clean);
}

export async function invoke(id, prompt, { executable, cwd, readOnly, timeoutMs, signal }) {
  const args = id === 'codex'
    ? ['exec', '--skip-git-repo-check', '--sandbox', readOnly ? 'read-only' : 'workspace-write',
      '-c', 'approval_policy="never"', '--json', '-']
    : ['-p', '--model', 'opus', '--output-format', 'stream-json', '--verbose',
      '--permission-mode', readOnly ? 'plan' : 'acceptEdits', '--permission-prompts', 'none'];
  // No shell interpolation; prompts go through stdin and each client keeps its own permission enforcement.
  let final = '', error = '', rateLimited = false;
  const outcome = await runProcess(executable, args, { cwd, input: prompt, timeoutMs, signal, onLine(line) {
    let event; try { event = JSON.parse(line); } catch { return; }
    if (id === 'codex' && event.type === 'item.completed' && event.item?.type === 'agent_message') final = event.item.text;
    if (id === 'claude' && event.type === 'result') { final = event.result ?? ''; if (event.is_error) error = (event.errors || [final]).join('\n'); }
    if (event.type === 'error' || event.type === 'turn.failed') error = event.message ?? event.error?.message ?? JSON.stringify(event.error ?? {});
    if (/usage.?limit|rate.?limit|quota.?exceed|out of.*credits|hit your limit/i.test(error)) rateLimited = true;
  } });
  return { ok: outcome.code === 0 && !outcome.reason && !error && Boolean(final),
    reason: outcome.reason ?? (rateLimited ? 'quota' : error ? 'provider-error' : outcome.code !== 0 ? 'exit-failed' : !final ? 'no-result' : null),
    text: final.slice(-64000), detail: error.slice(-2000), code: outcome.code };
}
