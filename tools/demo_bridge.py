"""End-to-end offline demo in fresh folders; no model, key, or network required."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from studio_runtime.adapters import Providers, run_command
from studio_runtime.contracts import load_config
from studio_runtime.engine import Bridge
from studio_runtime.store import Store

ROOT = Path(__file__).resolve().parents[1]
output = ROOT / '.studio-runtime' / ('demo-' + datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%f'))
output.mkdir(parents=True)
results = []
for kind in ('code', 'research'):
    workspace = output / kind
    workspace.mkdir()
    (workspace / 'kind.txt').write_text(kind)
    (workspace / 'inputs.json').write_text(json.dumps([{'name': 'A', 'count': 3}, {'name': 'B', 'count': 5}]))
    agent = {'provider': 'command', 'command': [sys.executable, str(ROOT / 'examples/demo_agent.py')],
             'probe_command': [sys.executable, str(ROOT / 'examples/demo_agent.py'), '--probe'],
             'capabilities': ['plan', 'review', 'research', 'write']}
    config = {'version': 1, 'agents': {'lead': agent, 'worker': agent}, 'lead_order': ['lead'],
              'worker_order': ['worker', 'lead'], 'checks': {'verify': [sys.executable, '-c',
                'from answer import unique_total; assert unique_total([1,1,2])==3; assert unique_total([-1,0,-1])==-1'
                if kind == 'code' else 'from pathlib import Path; s=Path("report.md").read_text(); assert "A: 3" in s and "B: 5" in s and "Total: 8" in s']}}
    config_path = workspace / 'config.json'
    config_path.write_text(json.dumps(config))
    store = Store(workspace / 'state')
    job = store.submit(workspace, 'Implement and test unique_total' if kind == 'code' else 'Summarize the supplied records with traceable totals')
    bridge = Bridge(store, load_config(config_path), Providers(), run_command)
    bridge.run()
    result = store.get(job['id'])
    results.append({'kind': kind, 'status': result['status'], 'calls': result['calls'], 'metrics': result['metrics'],
                    'routing': result['routing_metrics'], 'workspace': str(workspace)})
summary = {'mode': 'OFFLINE_FIXTURE_NOT_AI', 'results': results}
(output / 'result.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
raise SystemExit(0 if all(x['status'] == 'succeeded' for x in results) else 1)
