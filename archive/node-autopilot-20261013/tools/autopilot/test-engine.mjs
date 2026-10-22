import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, rm, readFile, mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { selectAgent, parseJson } from './providers.mjs';
import { enqueue, executeJob, claim, read, validatePlan, verifyProject } from './engine.mjs';
import { runProcess } from './process.mjs';

const policy = { priority: ['claude', 'codex', 'deepseek'], reservePercent: 5, quotaMaxAgeMs: 300000,
  maxCallsPerJob: 12, maxRepairRounds: 1, taskTimeoutMs: 10000, testTimeoutMs: 10000 };
const report = (...agents) => ({ agents: agents.map(([id, used = 10]) => ({ id, available: true,
  checkedAt: new Date().toISOString(), windows: [{ usedPercent: used }] })) });
async function fixture(t) {
  const root = await mkdtemp(join(tmpdir(), 'studio-auto-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const project = { path: root, allowedRoot: root, verify: [{ name: 'self-check', executable: process.execPath, args: ['-e', 'process.exit(0)'] }] };
  return { root, config: { ...policy, projects: { demo: project } }, job: await enqueue(root, 'demo', 'Write and test a small function') };
}
const plan = JSON.stringify({ steps: [{ title: 'implement', agent: 'codex', instructions: 'Write code and meaningful tests' }] });
const approved = JSON.stringify({ approved: true, summary: 'checked' });
const ok = text => ({ ok: true, text, reason: null });

test('fresh Opus wins; exhausted, absent, malformed and stale quota never means unlimited', () => {
  assert.equal(selectAgent(report(['claude'], ['codex']), policy), 'claude');
  assert.equal(selectAgent(report(['claude', 100], ['codex']), policy), 'codex');
  const stale = report(['claude']); stale.agents[0].checkedAt = '2020-01-01';
  assert.equal(selectAgent(stale, policy), null);
  const unknown = report(['claude']); unknown.agents[0].windows = [];
  assert.equal(selectAgent(unknown, policy), null);
  const reset = report(['claude']); reset.agents[0].windows[0].resetsAt = '2020-01-01';
  assert.equal(selectAgent(reset, policy), null);
  assert.equal(selectAgent(report(['claude', -1]), policy), null);
});
test('task schema and workspaces reject malformed or escaping requests', async t => {
  const f = await fixture(t);
  assert.throws(() => validatePlan({ steps: [] }, policy.priority));
  assert.throws(() => validatePlan({ steps: [{ instructions: 'bad', agent: 'shell' }] }, policy.priority));
  assert.throws(() => parseJson('I cannot do this'));
  await assert.rejects(enqueue(f.root, 'demo', '', 5));
  await assert.rejects(enqueue(f.root, 'demo', 'goal', 101));
  await mkdir(join(f.root, 'child'));
  await assert.rejects(verifyProject({ ...f.config.projects.demo, allowedRoot: join(f.root, 'child') }));
});
test('controller lock prevents two writers and can be released', async t => {
  const f = await fixture(t); const release = await claim(f.root);
  await assert.rejects(claim(f.root), /已运行/);
  await release(); await (await claim(f.root))();
});
test('real process tests run between AI implementation and review; checkpoint skips completed work', async t => {
  const f = await fixture(t); const stages = [];
  const result = await executeJob(f.job, f.config, f.root, { probe: async () => report(['codex']),
    call: async (id, prompt, options) => { stages.push([id, options.readOnly]); return ok(stages.length === 1 ? plan : stages.length === 2 ? 'Implemented' : approved); } });
  assert.equal(result.status, 'succeeded'); assert.equal(result.checks[0].code, 0);
  assert.deepEqual(stages, [['codex', true], ['codex', false], ['codex', true]]);
  const persisted = await read(join(f.root, 'jobs', f.job.id + '.json'));
  persisted.status = 'queued'; persisted.stage = 'test';
  let calls = 0;
  await executeJob(persisted, f.config, f.root, { probe: async () => report(['codex']), call: async () => { calls++; return ok(approved); } });
  assert.equal(calls, 1, 'does not rerun plan or completed worker');
});
test('Opus quota failure hands leadership to Codex with prior results', async t => {
  const f = await fixture(t); let calls = 0, handoff = '';
  const result = await executeJob(f.job, f.config, f.root, { probe: async () => report(['claude'], ['codex']), call: async (id, prompt) => {
    calls++;
    if (calls === 1) return { ok: false, reason: 'quota', text: 'Initial findings from Opus' };
    if (calls === 2) { assert.equal(id, 'codex'); handoff = prompt; return ok(plan); }
    return ok(calls === 3 ? 'Implemented' : approved);
  } });
  assert.equal(result.status, 'succeeded'); assert.equal(result.lead, 'codex');
  assert.match(handoff, /Initial findings from Opus/); assert.equal(calls, 4);
});
test('no available quota waits without model calls', async t => {
  const f = await fixture(t);
  const result = await executeJob(f.job, f.config, f.root, { probe: async () => report(['codex', 100]), call: () => assert.fail('must not infer') });
  assert.equal(result.status, 'waiting'); assert.equal(result.calls, 0);
});
test('failing tests cannot be overridden by AI approval; repair has a hard bound', async t => {
  const f = await fixture(t); let calls = 0;
  const result = await executeJob(f.job, f.config, f.root, { probe: async () => report(['codex']),
    call: async () => { calls++; return ok(calls === 1 ? plan : calls % 2 === 0 ? 'implementation' : approved); },
    test: async () => ({ code: 1, stdout: '', stderr: 'test failed', reason: null }) });
  assert.equal(result.status, 'needs-attention'); assert.equal(result.rounds, 1); assert.equal(calls, 5);
});
test('max inference budget stops additional calls', async t => {
  const f = await fixture(t); f.config.maxCallsPerJob = 1;
  const result = await executeJob(f.job, f.config, f.root, { probe: async () => report(['codex']), call: async () => ok(plan) });
  assert.equal(result.status, 'needs-attention'); assert.equal(result.calls, 1);
});
test('hidden process execution handles errors, timeout and abort', async () => {
  const okResult = await runProcess(process.execPath, ['-e', 'console.log("done")']); assert.equal(okResult.code, 0);
  const missing = await runProcess('does-not-exist-studio', []); assert.equal(missing.reason, 'launch-failed');
  const expired = await runProcess(process.execPath, ['-e', 'setInterval(()=>{},1000)'], { timeoutMs: 200 });
  assert.equal(expired.reason, 'timeout');
  const ctrl = new AbortController(); setTimeout(() => ctrl.abort(), 200);
  const cancelled = await runProcess(process.execPath, ['-e', 'setInterval(()=>{},1000)'], { signal: ctrl.signal });
  assert.equal(cancelled.reason, 'cancelled');
});
test('stop kills the child tree, not just its parent', async t => {
  const f = await fixture(t); const childPath = join(f.root, 'child.cjs'); const parentPath = join(f.root, 'parent.cjs');
  await writeFile(childPath, 'setInterval(()=>{},1000)');
  await writeFile(parentPath, 'const {spawn}=require("node:child_process");const c=spawn(process.execPath,[process.argv[2]],{windowsHide:true,stdio:"ignore"});console.log(c.pid);setInterval(()=>{},1000)');
  let pid; const ctrl = new AbortController();
  const result = await runProcess(process.execPath, [parentPath, childPath], { signal: ctrl.signal,
    onLine: line => { pid = Number(line); ctrl.abort(); } });
  assert.equal(result.reason, 'cancelled'); assert.ok(pid > 0);
  assert.throws(() => process.kill(pid, 0), { code: 'ESRCH' });
});
