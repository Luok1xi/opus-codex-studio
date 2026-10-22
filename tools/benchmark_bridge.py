"""Reproducible scheduler benchmark. Synthetic latency; never a model speed claim."""
import json
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tests.test_bridge import FakeProviders, task
from tools.studio_runtime.contracts import load_config
from tools.studio_runtime.engine import Bridge
from tools.studio_runtime.store import Store
from tools.studio_runtime.context import prompt_for

ROOT = Path(__file__).resolve().parents[1]
measurements = []
for parallel in (1, 3):
    for repeat in range(3):
        with TemporaryDirectory(prefix='studio-bench-') as tmp:
            config = load_config(ROOT / 'bridge.example.json')
            config['limits']['max_parallel'] = parallel
            config['agents']['researcher'] = dict(config['agents']['codex'], id='researcher')
            config['worker_order'].append('researcher')
            fake = FakeProviders()
            fake.pause = .12
            store = Store(Path(tmp) / 'state')
            job = store.submit(tmp, 'Independent input analysis', plan=[task('input-' + str(x)) for x in range(6)])
            bridge = Bridge(store, config, fake, lambda *a, **kw: {})
            started = time.perf_counter()
            result = bridge.execute(job)
            assert result['status'] == 'succeeded', result
            measurements.append({'parallel': parallel, 'seconds': round(time.perf_counter() - started, 4),
                                 'calls': result['calls'], 'quota_probes': fake.probes})
job['results'] = {str(x): {'status': 'succeeded', 'artifact': {'summary': 'x' * 5000, 'path': '/' + str(x)}} for x in range(20)}
naive = len(json.dumps(job['results']))
bounded = len(prompt_for(job, 'Read only the required evidence', 16000, ['3']))
report = {'mode': 'SYNTHETIC_SCHEDULER_NOT_MODEL_BENCHMARK', 'measurements': measurements,
          'context_example': {'all_results_chars': naive, 'one_dependency_prompt_chars': bounded}}
folder = ROOT / '.studio-runtime'
folder.mkdir(exist_ok=True)
(folder / 'benchmark.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
