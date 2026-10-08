"""Local studio checks only: no network, model calls, or game execution."""
import hashlib
import json
from pathlib import Path
from task_route import route_task
root = Path(__file__).resolve().parents[1]
c = json.loads((root / 'studio.config.json').read_text('utf-8'))
checks = {}
checks['entry_files'] = all((root / p).is_file() for p in ['AGENTS.md', 'CLAUDE.md', 'PROJECT_CONTEXT.md', 'STUDIO.md'])
checks['four_roles'] = len(c['roles']) == 4
checks['automation_off'] = all(c.get(k) is False for k in ['automatic_model_calls', 'hooks_enabled', 'github_actions_enabled', 'auto_merge'])
checks['green_codex_only'] = route_task('GREEN', config=c)['participants'] == ['codex']
checks['yellow_claude_only'] = route_task('YELLOW', config=c)['participants'] == ['claude']
checks['red_cap'] = route_task('RED', 2, c)['state'] == 'OWNER_DECISION'
lock = json.loads((root / 'studio/upstream.lock.json').read_text('utf-8'))
checks['upstream_integrity'] = all(hashlib.sha256((root / f['installed']).read_bytes()).hexdigest() == f['sha256'] for f in lock['files'])
checks['issue_templates'] = all((root / '.github/ISSUE_TEMPLATE' / (n + '.md')).is_file() for n in ['feature', 'scene', 'narrative-review', 'bug'])
checks['no_game_actions'] = not any((root / '.github/workflows').glob('*'))
for parent in (root, root.parent):
    p = parent / '.claude/settings.json'
    if p.exists():
        s = json.loads(p.read_text('utf-8-sig'))
        checks['no_hooks_' + parent.name] = not bool(s.get('hooks'))
result = {'scope': 'studio files and routing only', 'checks': checks, 'passed': all(checks.values()), 'model_calls': 0, 'not_verified': ['live Claude entry loading', 'gameplay', 'mobile layout', 'GitHub CLI authentication']}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(0 if result['passed'] else 1)
