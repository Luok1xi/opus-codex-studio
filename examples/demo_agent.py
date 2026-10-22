"""OFFLINE FIXTURE, not an AI. Exercises the public command-adapter protocol."""
import json
import sys
import time
from pathlib import Path

if '--probe' in sys.argv:
    print(json.dumps({'available': True, 'reason': 'offline fixture', 'observed_at': time.time(),
                      'windows': [{'remaining_percent': 100, 'reset_at': None}]}))
    raise SystemExit

request = json.load(sys.stdin)
prompt = request['prompt']
folder = Path(request['cwd'])
kind = (folder / 'kind.txt').read_text().strip()
time.sleep(.04)
if 'Act as lead.' in prompt:
    text = json.dumps({'tasks': [
        {'id': 'inspect-a', 'instruction': 'Inspect first input', 'depends_on': [], 'capabilities': ['research'], 'read_only': True},
        {'id': 'inspect-b', 'instruction': 'Inspect second input', 'depends_on': [], 'capabilities': ['research'], 'read_only': True},
        {'id': 'produce', 'instruction': 'Produce the requested artifact', 'depends_on': ['inspect-a', 'inspect-b'], 'capabilities': ['write'], 'read_only': False}]})
elif 'Review the actual outputs' in prompt:
    output = folder / ('answer.py' if kind == 'code' else 'report.md')
    text = json.dumps({'approved': output.is_file(), 'summary': 'Offline fixture reviewed the actual output', 'repair': 'Create the missing output'})
elif not request['read_only']:
    if kind == 'code':
        (folder / 'answer.py').write_text('def unique_total(values):\n    return sum(set(values))\n', encoding='utf-8')
        text = 'Created answer.py; mechanical verification checks duplicate and negative inputs.'
    else:
        items = json.loads((folder / 'inputs.json').read_text())
        (folder / 'report.md').write_text('# Evidence report\n\n' + '\n'.join(f'- {x["name"]}: {x["count"]}' for x in items)
                                          + f'\n\nTotal: {sum(x["count"] for x in items)}\n', encoding='utf-8')
        text = 'Created report.md with all source items and their total.'
else:
    text = 'Inspected the fixture input without modifying it.'
print(json.dumps({'status': 'succeeded', 'text': text, 'usage': {}, 'session_id': None}))
