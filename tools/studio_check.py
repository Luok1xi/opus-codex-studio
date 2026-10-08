"""Check the reusable studio package; no model, network or game execution."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    root = Path(root).resolve()
    failures = []
    required = ['README.md', 'AGENTS.md', 'CLAUDE.md', 'STUDIO.md',
                'PROJECT_CONTEXT.md', 'production/OPUS_TO_CODEX.md',
                'production/CODEX_TO_OPUS.md', 'production/BOARD.md',
                'tools/studio/codex_dispatch.ps1', 'THIRD_PARTY_NOTICES.md']
    failures.extend('missing: ' + rel for rel in required if not (root/rel).is_file())
    try:
        cfg = json.loads((root/'studio.config.json').read_text('utf-8'))
        if cfg.get('lead') != 'claude-opus' or cfg.get('codex_role') != 'on-request-support':
            failures.append('invalid current roles')
        for flag in ['automatic_model_calls', 'hooks_enabled', 'github_actions_enabled', 'auto_merge']:
            if cfg.get(flag) is not False:
                failures.append('unexpected automation: ' + flag)
    except (OSError, ValueError):
        failures.append('invalid config')
    checked = 0
    for lock_name, prefix, path_key in [
            ('studio/upstream.lock.json', '', 'installed'),
            ('studio/game-art-workflows.lock.json', 'studio/vendor/gamedev-skills/', 'path')]:
        try:
            lock = json.loads((root/lock_name).read_text('utf-8'))
            if len(lock['commit']) != 40 or any(c not in '0123456789abcdef' for c in lock['commit']):
                failures.append('invalid pinned commit: ' + lock_name)
            for item in lock['files']:
                path = (root / (prefix + item[path_key])).resolve()
                if not path.is_relative_to(root):
                    failures.append('path outside package: ' + lock_name)
                    continue
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                    failures.append('vendor hash mismatch: ' + path.relative_to(root).as_posix())
                checked += 1
        except (OSError, ValueError, KeyError, TypeError):
            failures.append('invalid vendor lock: ' + lock_name)
    return {'scope': 'STUDIO_PACKAGE_ONLY', 'status': 'FAIL' if failures else 'PASS',
            'vendor_files_checked': checked, 'failures': failures}


if __name__ == '__main__':
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if result['failures'] else 0)
