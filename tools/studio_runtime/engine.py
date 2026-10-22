"""A mechanical bridge: models plan/review, Python schedules and runs checks."""
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path

from .context import artifact, prompt_for
from .contracts import parse_json, validate_plan
from .routing import Router
from .store import controller_lock


class Bridge:
    def __init__(self, store, config, providers, check_runner):
        self.store, self.config, self.providers = store, config, providers
        self.check_runner = check_runner
        self.router = Router(config, providers)
        self.cancel = threading.Event()

    def _save(self, job, event=None, **detail):
        job['routing_metrics'] = dict(self.router.stats)
        self.store.save(job, event, detail)

    def _prepare(self, job, instruction, dependencies=None):
        if job['calls'] >= self.config['limits']['max_calls']:
            raise ValueError('Model call budget exhausted')
        prompt = prompt_for(job, instruction, self.config['limits']['context_chars'], dependencies)
        job['calls'] += 1
        job['metrics']['prompt_chars'] += len(prompt)
        return prompt

    def _invoke(self, name, prompt, job, read_only, session=None):
        try:
            return self.providers.invoke(self.config['agents'][name], prompt, cwd=job['workspace'],
                                         read_only=read_only, session_id=session, cancel=self.cancel,
                                         timeout=self.config['limits']['timeout_seconds'])
        except Exception:
            return {'status': 'failed', 'text': 'Provider invocation failed; check client readiness.', 'elapsed_ms': 0}

    def _record(self, job, key, name, result, attempt=None):
        record = {key: result.get(key) for key in ('status', 'session_id', 'usage', 'elapsed_ms')}
        record['attempt'] = job['calls'] if attempt is None else attempt
        if record['status'] not in ('succeeded', 'quota', 'auth', 'failed', 'cancelled', 'timeout'):
            record['status'] = 'failed'
        record['agent'] = name
        record['artifact'] = artifact(self.store.root, str(result.get('text', ''))[:1000000])
        job['results'][key] = record
        job['metrics']['model_ms'] += max(0, result.get('elapsed_ms', 0) or 0)
        self._save(job, 'attempt-finished', task=key, agent=name, attempt=record['attempt'],
                   status=record['status'], artifact=record['artifact']['sha256'])
        return record

    def _lead(self, job, instruction):
        for _ in self.config['agents']:
            if self.cancel.is_set():
                return None
            name = self.router.select('lead', ['plan' if job['phase'] == 'plan' else 'review'], job.get('lead'))
            if not name:
                job['status'] = 'waiting'
                self._save(job, 'lead-unavailable')
                return None
            if job.get('lead') != name:
                before, job['lead'] = job.get('lead'), name
                self._save(job, 'lead-changed', previous=before, current=name)
            prompt = self._prepare(job, instruction)
            self._save(job, 'attempt-started', task=job['phase'], agent=name, attempt=job['calls'])
            session_key = job['phase'] + ':' + name
            result = self._invoke(name, prompt, job, True, job.get('role_sessions', {}).get(session_key))
            self._record(job, job['phase'] + '-' + str(job['calls']), name, result)
            if result.get('session_id'):
                job.setdefault('role_sessions', {})[session_key] = result['session_id']
            if result['status'] == 'succeeded':
                return parse_json(result['text'])
            if result['status'] in ('quota', 'auth'):
                self.router.reject(name, result['status'])
                job['last_error'] = {'agent': name, 'status': result['status'], 'phase': job['phase']}
                continue
            job['status'] = 'cancelled' if result['status'] == 'cancelled' else 'needs-attention'
            return None
        job['status'] = 'waiting'
        return None

    def _work(self, job):
        tasks = job['tasks']
        for task in tasks:
            task.setdefault('state', 'pending')
        with ThreadPoolExecutor(max_workers=self.config['limits']['max_parallel']) as pool:
            active = {}
            dispatch_error = None
            while not self.cancel.is_set():
                succeeded = {task['id'] for task in tasks if task['state'] == 'succeeded'}
                for task in ([] if dispatch_error or any(t['state'] == 'uncertain' for t in tasks) else tasks):
                    if len(active) >= self.config['limits']['max_parallel']:
                        break
                    if task['state'] != 'pending' or not set(task['depends_on']) <= succeeded:
                        continue
                    # Same-workspace writers exclude readers too; nobody reads a half-written artifact.
                    if active and (not task['read_only'] or any(not item['read_only'] for item, _ in active.values())):
                        continue
                    busy = [name for _, name in active.values()]
                    name = self.router.select('worker', task['capabilities'], task.get('agent'), busy)
                    if not name:
                        continue
                    try:
                        dependencies = list(task['depends_on'])
                        if task['id'] in job['results']:
                            dependencies.append(task['id'])
                        prompt = self._prepare(job, task['instruction'], None if job['repairs'] else dependencies)
                    except ValueError as error:
                        dispatch_error = str(error)
                        break
                    task['state'] = 'running'
                    task['attempt'] = job['calls']
                    self._save(job, 'attempt-started', task=task['id'], agent=name, attempt=task['attempt'])
                    future = pool.submit(self._invoke, name, prompt, job, task['read_only'], task.get('sessions', {}).get(name))
                    active[future] = (task, name)
                    job['metrics']['max_parallel_observed'] = max(job['metrics']['max_parallel_observed'], len(active))
                if not active:
                    if any(task['state'] == 'uncertain' for task in tasks):
                        job['status'] = 'needs-reconciliation'
                        self._save(job, 'effect-uncertain', message='A writer may have acted; verify its effects before retrying or repairing.')
                    elif dispatch_error:
                        job['status'] = 'needs-attention'
                        self._save(job, 'dispatch-stopped', message=dispatch_error)
                    elif all(task['state'] == 'succeeded' for task in tasks):
                        job['phase'] = 'checks'
                    elif any(task['state'] == 'failed' for task in tasks):
                        job['phase'] = 'review'
                    else:
                        job['status'] = 'waiting'
                    self._save(job, 'work-checkpoint')
                    return
                done, _ = wait(active, timeout=.2, return_when=FIRST_COMPLETED)
                for future in done:
                    task, name = active.pop(future)
                    result = future.result()
                    receipt = self._record(job, task['id'], name, result, task['attempt'])
                    if result.get('session_id'):
                        task.setdefault('sessions', {})[name] = result['session_id']
                    if not task['read_only'] and receipt['status'] != 'succeeded':
                        # A CLI can fail after committing an action. Neither fallback nor repair may replay it blindly.
                        task['state'] = 'uncertain'
                        job['last_error'] = {'task': task['id'], 'agent': name, 'status': receipt['status'],
                                             'partial_result': receipt['artifact']}
                    elif receipt['status'] in ('quota', 'auth'):
                        self.router.reject(name, receipt['status'])
                        task['state'] = 'pending'
                        job['last_error'] = {'task': task['id'], 'agent': name, 'status': receipt['status'],
                                             'partial_result': receipt['artifact']}
                    else:
                        task['state'] = 'succeeded' if receipt['status'] == 'succeeded' else 'failed'
                    self._save(job, 'task-checkpoint', task=task['id'], state=task['state'])
            # Cancelling the shared event terminates each adapter's owned process tree before releasing the lock.
            for future, (task, name) in active.items():
                self._record(job, task['id'], name, future.result(), task['attempt'])
                task['state'] = 'cancelled'

    def execute(self, job):
        job['status'] = 'running'
        self._save(job, 'job-started')
        try:
            while job['status'] == 'running' and not self.cancel.is_set():
                phase = job['phase']
                if phase == 'plan':
                    schema = {'tasks': [{'id': 'task1', 'instruction': 'Specific task and acceptance criteria',
                                          'depends_on': [], 'capabilities': ['write'], 'read_only': False}]}
                    plan = self._lead(job, 'Act as lead. Inspect the workspace read-only. Return ONLY JSON in this shape: '
                                      + json.dumps(schema) + '. Use a small task graph, batch tiny steps, independent read-only research can run together. '
                                      + 'Capabilities available: ' + json.dumps({k: v['capabilities'] for k, v in self.config['agents'].items()})
                                      + '. Commands for checks are configured separately; do not invent executable commands in the plan.')
                    if plan is None:
                        break
                    job['tasks'] = validate_plan(plan, self.config)
                    job['phase'] = 'work'
                    self._save(job, 'plan-accepted')
                elif phase == 'work':
                    self._work(job)
                elif phase == 'checks':
                    job['checks'] = []
                    for name, command in self.config['checks'].items():
                        if self.cancel.is_set():
                            break
                        result = self.check_runner(command, cwd=job['workspace'], cancel=self.cancel,
                                                   timeout=self.config['limits']['timeout_seconds'])
                        text = (result.get('stdout', '') + '\n' + result.get('stderr', ''))[-1000000:]
                        job['checks'].append({'name': name, 'code': result.get('code'), 'status': result['status'],
                                              'artifact': artifact(self.store.root, text)})
                        self._save(job, 'check-finished', name=name, status=result['status'])
                    job['phase'] = 'review'
                elif phase == 'review':
                    checks_pass = len(job.get('checks', [])) == len(self.config['checks']) and all(
                        x['status'] == 'succeeded' and x['code'] == 0 for x in job.get('checks', []))
                    tasks_pass = all(t.get('state') == 'succeeded' for t in job['tasks'])
                    if not (checks_pass and tasks_pass) and job['repairs'] >= self.config['limits']['max_repairs']:
                        job['status'] = 'needs-attention'
                        self._save(job, 'review-skipped', reason='Hard failure and no repair budget; approval cannot change the outcome.')
                        break
                    result = self._lead(job, 'Review the actual outputs read-only against the original goal. '
                                        'Return ONLY JSON {"approved":true|false,"summary":"evidence and limits",'
                                        '"repair":"specific corrections if needed"}. A process exit alone does not prove quality.')
                    if result is None:
                        break
                    if type(result.get('approved')) is not bool or not isinstance(result.get('summary'), str):
                        raise ValueError('Invalid review contract')
                    job['review'] = result
                    if result['approved'] and checks_pass and tasks_pass:
                        job['status'] = 'succeeded'
                    elif job['repairs'] < self.config['limits']['max_repairs']:
                        job['repairs'] += 1
                        if all(task['read_only'] for task in job['tasks']):
                            # Keep specialist capabilities and dependency order; repair grants no new permissions.
                            repair_tasks = job['tasks']
                        else:
                            repair_tasks = [{'id': 'repair-' + str(job['repairs']),
                                'instruction': 'Complete the original goal and correct the review findings.',
                                'depends_on': [], 'capabilities': ['write'], 'read_only': False}]
                        job['tasks'] = validate_plan({'tasks': repair_tasks}, self.config)
                        job['phase'] = 'work'
                    else:
                        job['status'] = 'needs-attention'
                    self._save(job, 'review-recorded', approved=result['approved'])
                else:
                    raise ValueError('Unknown phase')
        except (ValueError, TypeError, KeyError) as exc:
            job['status'] = 'needs-attention'
            self._save(job, 'contract-error', message=str(exc))
        if self.cancel.is_set():
            job['status'] = 'cancelled'
        self._save(job, 'job-finished', status=job['status'])
        return job

    def run(self, watch=False):
        with controller_lock(self.store.root):
            self.store.recover_interrupted(self.config['limits']['max_recoveries'])
            stop = self.store.root / 'stop.request'
            stop.unlink(missing_ok=True)
            finished = threading.Event()

            def monitor():
                while not finished.wait(.2):
                    if stop.exists():
                        self.cancel.set()
                        return

            monitor_thread = threading.Thread(target=monitor, daemon=True)
            monitor_thread.start()
            try:
                while not self.cancel.is_set():
                    ready = self.store.list(ready=True)
                    if ready:
                        self.execute(ready[0])
                    elif not watch:
                        break
                    else:
                        # Idle waiting makes no model calls and performs no quota probes.
                        self.cancel.wait(2)
            finally:
                finished.set()
                monitor_thread.join(1)
