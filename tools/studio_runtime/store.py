"""SQLite checkpoints and process-held locks: a crash never silently replays work."""
import json
import hashlib
import os
import re
import sqlite3
import time
import uuid
from contextlib import contextmanager
from pathlib import Path


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / 'studio.sqlite3'
        with self.connect() as db:
            db.executescript('''
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS jobs(
                  id TEXT PRIMARY KEY, request_key TEXT UNIQUE NOT NULL, workspace TEXT NOT NULL,
                  status TEXT NOT NULL, priority INTEGER NOT NULL, updated REAL NOT NULL, data TEXT NOT NULL);
                CREATE INDEX IF NOT EXISTS ready_jobs ON jobs(status, priority DESC, updated);
                CREATE TABLE IF NOT EXISTS events(
                  seq INTEGER PRIMARY KEY AUTOINCREMENT, job TEXT, at REAL NOT NULL, kind TEXT NOT NULL, data TEXT NOT NULL);
                CREATE INDEX IF NOT EXISTS job_events ON events(job, seq);
            ''')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def submit(self, workspace, goal, priority=50, request_key=None, plan=None, kind='workflow'):
        if kind not in ('workflow', 'consult'):
            raise ValueError('Unknown job kind')
        path = Path(workspace).resolve(strict=True)
        if not path.is_dir() or not isinstance(goal, str) or not 1 <= len(goal.strip()) <= 32000:
            raise ValueError('An existing workspace and a nonempty bounded goal are required')
        if type(priority) is not int or not 0 <= priority <= 100:
            raise ValueError('priority must be 0–100')
        request_key = request_key or str(uuid.uuid4())
        if not isinstance(request_key, str) or not 1 <= len(request_key) <= 200:
            raise ValueError('Invalid request key')
        fingerprint = hashlib.sha256(json.dumps([str(path), goal, priority, plan], sort_keys=True).encode()).hexdigest()
        if kind != 'workflow':
            fingerprint = hashlib.sha256((kind + fingerprint).encode()).hexdigest()
        job = {'id': str(uuid.uuid4()), 'request_key': request_key, 'request_fingerprint': fingerprint, 'workspace': str(path), 'goal': goal,
               'priority': priority, 'kind': kind, 'status': 'queued' if kind == 'workflow' else 'consult-pending',
               'phase': 'work' if plan else 'plan', 'lead': None,
               'calls': 0, 'repairs': 0, 'tasks': plan or [], 'results': {}, 'updated': time.time(),
               'metrics': {'prompt_chars': 0, 'model_ms': 0, 'max_parallel_observed': 0}}
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT data FROM jobs WHERE request_key=?', (request_key,)).fetchone()
            if row:
                existing = json.loads(row['data'])
                if existing.get('request_fingerprint') != fingerprint:
                    raise ValueError('Request key was already used for a different task')
                return existing
            db.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?,?)', (job['id'], request_key, str(path), job['status'], priority,
                                                                  job['updated'], json.dumps(job)))
        return job

    def get(self, job_id):
        with self.connect() as db:
            row = db.execute('SELECT data FROM jobs WHERE id=?', (job_id,)).fetchone()
        if not row:
            raise ValueError('Unknown job')
        return json.loads(row['data'])

    def save(self, job, event=None, detail=None):
        job['updated'] = time.time()
        with self.connect() as db:
            db.execute('UPDATE jobs SET status=?,updated=?,data=? WHERE id=?',
                       (job['status'], job['updated'], json.dumps(job), job['id']))
            if event:
                db.execute('INSERT INTO events(job,at,kind,data) VALUES(?,?,?,?)',
                           (job['id'], time.time(), event, json.dumps(detail or {})))

    def list(self, ready=False):
        sql = 'SELECT data FROM jobs'
        if ready:
            sql += " WHERE status='queued' OR (status='waiting' AND updated<?)"
        sql += ' ORDER BY priority DESC,updated LIMIT 100'
        with self.connect() as db:
            rows = db.execute(sql, (time.time() - 60,) if ready else ()).fetchall()
        return [json.loads(row['data']) for row in rows]

    def _valid_receipt(self, receipt, attempt):
        if not isinstance(receipt, dict) or receipt.get('status') != 'succeeded' or type(attempt) is not int or receipt.get('attempt') != attempt:
            return False
        evidence = receipt.get('artifact')
        sha = evidence.get('sha256', '') if isinstance(evidence, dict) else ''
        if not isinstance(sha, str) or not re.fullmatch('[0-9a-f]{64}', sha):
            return False
        path = self.root / 'artifacts' / (sha + '.txt')
        try:
            return path.stat().st_size <= 4000000 and hashlib.sha256(path.read_bytes()).hexdigest() == sha
        except OSError:
            return False

    def recover_interrupted(self, max_recoveries=0):
        with self.connect() as db:
            rows = db.execute("SELECT data FROM jobs WHERE status='running'").fetchall()
        for row in rows:
            job = json.loads(row['data'])
            if job.get('kind') == 'consult':
                job['status'] = 'needs-reconciliation'
                self.save(job, 'consult-interrupted', {'reason': 'Consultations are never automatically replayed.'})
                continue
            reasons = []
            if job.get('recoveries', 0) >= max_recoveries:
                reasons.append('Automatic recovery budget exhausted')
            if job.get('phase') not in ('plan', 'work', 'review'):
                # Owner-configured check commands may write too; their effects are not inferred from their names.
                reasons.append('Interrupted phase has no replay guarantee')
            for task in job.get('tasks', []):
                if task.get('state') == 'uncertain':
                    reasons.append('Writer requires reconciliation: ' + task['id'])
                if task.get('state') != 'running':
                    continue
                receipt = job.get('results', {}).get(task['id'], {})
                if self._valid_receipt(receipt, task.get('attempt')):
                    task['state'] = 'succeeded'
                elif task.get('read_only') is True:
                    task['state'] = 'pending'
                else:
                    task['state'] = 'uncertain'
                    reasons.append('Writer has no matching verified receipt: ' + task['id'])
            if reasons:
                job['status'] = 'needs-reconciliation' if any(t.get('state') == 'uncertain' for t in job.get('tasks', [])) else 'interrupted'
                self.save(job, 'controller-interrupted', {'reasons': reasons})
            else:
                job['recoveries'] = job.get('recoveries', 0) + 1
                job['status'] = 'queued'
                self.save(job, 'controller-recovered', {'recoveries': job['recoveries'], 'calls_already_used': job['calls']})

    def events(self, job_id, after=0, limit=50):
        with self.connect() as db:
            rows = db.execute('SELECT * FROM events WHERE job=? AND seq>? ORDER BY seq LIMIT ?',
                              (job_id, after, min(limit, 100))).fetchall()
        return [dict(row) | {'data': json.loads(row['data'])} for row in rows]


@contextmanager
def controller_lock(root):
    path = Path(root) / 'controller.lock'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as handle:
        if path.stat().st_size == 0:
            handle.write(b'0')
            handle.flush()
        handle.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise RuntimeError('Another bridge already owns this state directory') from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)
