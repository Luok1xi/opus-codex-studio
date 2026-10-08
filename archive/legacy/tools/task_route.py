"""Print a bounded handoff plan. Never launches a model or external process."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def route_task(level, completed_rounds=0, config=None):
    if config is None:
        config = json.loads((ROOT / 'studio.config.json').read_text(encoding='utf-8'))
    if level not in ('GREEN', 'YELLOW', 'ORANGE', 'RED'):
        raise ValueError('Unknown task level')
    if isinstance(completed_rounds, bool) or not isinstance(completed_rounds, int) or completed_rounds < 0:
        raise ValueError('completed_rounds must be a non-negative integer')
    if config.get('automatic_model_calls') is not False:
        raise ValueError('Automatic model calls must remain disabled')
    if config.get('max_red_rounds') != 2:
        raise ValueError('Project requires a two-round RED cap')
    owners = {'GREEN': ['codex'], 'YELLOW': ['claude'],
              'ORANGE': ['chatgpt-scene-card', 'claude-draft', 'chatgpt-review'],
              'RED': ['chatgpt', 'claude', 'creative-owner']}
    if config.get('routes') != owners:
        raise ValueError('Routing changed; reconcile with STUDIO.md before proceeding')
    escalation = level == 'RED' and completed_rounds >= 2
    return {
        'level': level,
        'state': 'OWNER_DECISION' if escalation else 'MANUAL_HANDOFF',
        'participants': ['creative-owner'] if escalation else owners[level],
        'remaining_rounds': max(0, 2 - completed_rounds) if level == 'RED' else None,
        'automatic_model_calls': 0,
        'executes_work': False,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('level', choices=['GREEN', 'YELLOW', 'ORANGE', 'RED'])
    parser.add_argument('--completed-rounds', type=int, default=0)
    args = parser.parse_args()
    try:
        result = route_task(args.level, args.completed_rounds)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
