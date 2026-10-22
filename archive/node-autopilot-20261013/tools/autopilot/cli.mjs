import { readFile, mkdir, writeFile, access, unlink } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { join, resolve } from 'node:path';
import { setTimeout as delay } from 'node:timers/promises';
import { doctor, discover } from './providers.mjs';
import { read, save, jobs, claim, enqueue, executeJob, verifyProject } from './engine.mjs';

const studio = fileURLToPath(new URL('../../', import.meta.url));
const config = (await read(join(studio, 'studio.config.json'))).autopilot;
const runtime = join(studio, 'runtime/autopilot');
const [command = 'status', ...args] = process.argv.slice(2);
const stopFile = join(runtime, 'stop');
await mkdir(runtime, { recursive: true });

async function writeStatus() {
  const all = await jobs(runtime);
  let health; try { health = await read(join(runtime, 'health.json')); } catch { health = null; }
  let controller; try { controller = await read(join(runtime, 'controller.lock')); } catch { controller = null; }
  const result = { controller, health, jobs: all.sort((a, b) => b.createdAt.localeCompare(a.createdAt))
    .map(({ id, project, goal, status, stage, step, calls, lead, review }) => ({ id, project, goal, status, stage, step, calls, lead, review })) };
  await save(join(runtime, 'status.json'), result);
  return result;
}

try {
  if (command === 'doctor') {
    const result = await doctor(); await save(join(runtime, 'health.json'), result);
    console.log(JSON.stringify(result, null, 2));
  } else if (command === 'enqueue') {
    const [project, goalFile, priority = '50'] = args;
    await verifyProject(config.projects[project]);
    if (!goalFile) throw new Error('用法：enqueue 项目名 任务文本文件 [0–100优先级]');
    const job = await enqueue(runtime, project, await readFile(resolve(goalFile), 'utf8'), Number(priority));
    console.log(JSON.stringify({ id: job.id, status: job.status, project }));
  } else if (command === 'run' || command === 'watch') {
    if (!config?.enabled || config.authorization !== 'owner-local-development-2026-10-13') throw new Error('尚未配置本地自动调用授权');
    const release = await claim(runtime);
    const controller = new AbortController();
    const stop = () => controller.abort();
    process.once('SIGINT', stop); process.once('SIGTERM', stop);
    await unlink(stopFile).catch(error => { if (error.code !== 'ENOENT') throw error; });
    let checking = false;
    const timer = setInterval(async () => {
      if (checking) return;
      checking = true;
      try { await access(stopFile); stop(); } catch { /* no stop request */ }
      finally { checking = false; }
    }, 500);
    const executables = discover();
    try {
      // Interrupted work is never silently relaunched after a crash.
      for (const job of await jobs(runtime)) if (job.status === 'running') {
        job.status = 'needs-attention'; job.events.push({ event: 'interrupted-controller', at: new Date().toISOString() });
        await save(join(runtime, 'jobs', job.id + '.json'), job);
      }
      do {
        const candidates = (await jobs(runtime)).filter(j => j.status === 'queued'
          || j.status === 'waiting' && Date.now() - Date.parse(j.updatedAt) > 90000)
          .sort((a, b) => b.priority - a.priority || a.createdAt.localeCompare(b.createdAt));
        if (candidates.length) {
          const job = candidates[0];
          try { await executeJob(job, config, runtime, { signal: controller.signal, executables }); }
          catch (error) { job.status = 'needs-attention'; job.events.push({ event: 'configuration-error', message: error.message }); await save(join(runtime, 'jobs', job.id + '.json'), job); }
          console.log(JSON.stringify({ id: job.id, status: job.status, lead: job.lead, calls: job.calls }));
        }
        await writeStatus();
        if (command === 'run' && !candidates.length) break;
        if (!candidates.length) await delay(3000, undefined, { signal: controller.signal }).catch(() => {});
      } while (!controller.signal.aborted);
    } finally { clearInterval(timer); await release(); await writeStatus(); }
  } else if (command === 'stop') {
    await writeFile(stopFile, new Date().toISOString()); console.log('已请求停止；当前进程树会结束，完成的步骤保留。');
  } else if (command === 'recover') {
    const lock = await read(join(runtime, 'controller.lock'));
    try { process.kill(lock.pid, 0); throw new Error('原进程仍存在，不回收锁也不自动杀进程'); }
    catch (error) { if (error.code !== 'ESRCH') throw error; }
    await unlink(join(runtime, 'controller.lock'));
    for (const job of await jobs(runtime)) if (job.status === 'running') {
      job.status = 'needs-attention'; job.events.push({ event: 'crash-recovered', at: new Date().toISOString() });
      await save(join(runtime, 'jobs', job.id + '.json'), job);
    }
    console.log('已回收失效锁；中断任务保留待检查，不重复执行。');
  } else if (command === 'status') console.log(JSON.stringify(await writeStatus(), null, 2));
  else throw new Error('支持 doctor / enqueue / run / watch / status / stop / recover');
} catch (error) { console.error(error.message); process.exitCode = 1; }
