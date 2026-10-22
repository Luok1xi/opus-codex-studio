"""One explicit consultation, saved in the shared ledger without automatic replay."""
import time

from .context import artifact
from .store import controller_lock


def consult(store, invoke, *, workspace, prompt, connection, session=None, timeout=120, key=None):
    # Headless tools inherit Harness permissions, so this is not labelled read-only.
    task = {'id': 'consult', 'instruction': prompt, 'depends_on': [], 'capabilities': [],
            'read_only': False, 'connection': str(connection), 'session': session, 'timeout': timeout}
    with controller_lock(store.root):
        job = store.submit(workspace, prompt, request_key=key, plan=[task], kind='consult')
        if job['calls']:
            return job  # A lost reply must not purchase or repeat the same work again.
        job.update(status='running', calls=1)
        job['tasks'][0].update(state='running', attempt=1)
        job['metrics']['prompt_chars'] = len(prompt)
        store.save(job, 'consult-started', {'agent': 'deepseek', 'attempt': 1})
        started = time.monotonic()
        try:
            result = invoke(connection, prompt, workspace=workspace, session=session, timeout=timeout)
            evidence = artifact(store.root, result.get('text', ''))
            job['results']['consult'] = {k: result.get(k) for k in ('status', 'session_id', 'diagnostic')}
            job['results']['consult'].update(agent='deepseek', attempt=1, artifact=evidence)
            # An answer is evidence for the operator, not an independently accepted deliverable.
            job['status'] = 'answered' if result['status'] == 'succeeded' else 'needs-reconciliation'
        finally:
            if job['status'] == 'running':
                job['status'] = 'needs-reconciliation'
            job['tasks'][0]['state'] = 'succeeded' if job['status'] == 'answered' else 'uncertain'
            job['metrics']['model_ms'] = round((time.monotonic() - started) * 1000)
            store.save(job, 'consult-finished', {'status': job['status']})
        return job
