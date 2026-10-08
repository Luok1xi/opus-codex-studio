"""Validate project scaffolding only; never claim game or Windows runtime QA."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    root = root.resolve()
    failures = []
    checks = []

    def check(name, ok):
        checks.append({'check': name, 'status': 'PASS' if ok else 'FAIL'})
        if not ok:
            failures.append(name)

    required = ['README.md', 'PROJECT_CONTEXT.md', 'AGENTS.md', 'STUDIO.md', 'CLAUDE.md',
                'bible/THEME.md', 'bible/NARRATIVE_RULES.md', 'bible/WORLD.md',
                'bible/FORBIDDEN_CLICHES.md', 'characters/liwei.md', 'characters/shiori.md',
                'characters/heroine.md', 'characters/narrator.md', 'mystery/clue_map.md',
                'mystery/narrator_knowledge.md', 'mystery/second_playthrough.md',
                'templates/SCENE_CARD.md', 'templates/MYSTERY_BOARD.md',
                'templates/RELATIONSHIP_MATERIAL_CARD.md', 'production/MILESTONES.md',
                'outline/scene_list.md', 'production/github-bootstrap.json',
                'reviews/BOOTSTRAP_REPORT.md']
    missing = [p for p in required if not (root/p).is_file()]
    check('required_project_files', not missing)
    try:
        cfg = json.loads((root/'studio.config.json').read_text(encoding='utf-8'))
        check('four_roles_only', set(cfg['roles']) == {'creative-owner','showrunner','lead-writer','technical-director-narrative-qa'} and len(cfg['roles']) == 4)
        check('two_round_red_cap', cfg['max_red_rounds'] == 2)
        check('one_orange_review', cfg['max_orange_reviews'] == 1)
        flags = ['automatic_model_calls', 'hooks_enabled', 'github_actions_enabled',
                 'mcp_enabled', 'review_gate_enabled', 'auto_merge']
        check('automatic_execution_off', all(cfg.get(flag) is False for flag in flags))
        check('only_three_mechanics', cfg['mechanics'] == ['feedback-misreading','heroine-crosses-options','replay-without-narrator'])
        check('deadline_china_time', cfg['delivery_before'] == '2026-10-02T00:00:00+08:00')
    except (OSError, ValueError, KeyError, TypeError):
        check('config_parse', False)
    for name in ('feature', 'scene', 'narrative-review', 'bug'):
        check('issue_template_' + name, (root/f'.github/ISSUE_TEMPLATE/{name}.md').is_file())
    check('eight_scene_cards', sorted(p.name for p in (root/'outline/cards').glob('*.md')) == [f'S{i:02}.md' for i in range(1, 9)])
    # Script writing is authorized; accepting existing drafts must not fail bootstrap QA.
    check('script_directory_present', (root/'script').is_dir())
    check('no_github_actions', not any((root/'.github/workflows').glob('*.y*ml')))
    check('no_agent_autorun_configuration', all(not (root/p).exists() for p in
        ['.claude/settings.json','.claude/agents','.claude/hooks','.mcp.json','hooks.json','.codex/config.toml']))
    try:
        lock = json.loads((root/'studio/upstream.lock.json').read_text(encoding='utf-8'))
        check('upstream_commit_pinned', len(lock['commit']) == 40 and all(c in '0123456789abcdef' for c in lock['commit']))
        for item in lock['files']:
            path = (root/item['installed']).resolve()
            safe = root in path.parents
            ok = safe and path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']
            check('upstream_hash_' + Path(item['installed']).name, ok)
    except (OSError, ValueError, KeyError, TypeError):
        check('upstream_manifest', False)
    required_lines = ['不是因为我做对了，她才爱我。','我又不是在和他谈恋爱。','我是在和她谈。',
                      '她又不是客服。','我不知道啊。','那就先别相信自己了。','我替你记得一会儿。',
                      '因为我们是恋人。','一朵就够了。',
                      '你一直都在选。怎么哄我，怎么陪我，怎么让我开心。可我也一直在选啊。']
    narrative = (root/'bible/NARRATIVE_RULES.md').read_text(encoding='utf-8') if (root/'bible/NARRATIVE_RULES.md').exists() else ''
    check('all_required_lines_preserved', all(line in narrative for line in required_lines))
    return {'scope':'LOCAL_STUDIO_CONFIGURATION_ONLY','status':'FAIL' if failures else 'PASS',
            'checks':checks,'failures':failures,'missing':missing,
            'not_run':['Windows host installation','Claude Code live session','GitHub issue/milestone/PR','Mobile GitHub UI','Web game runtime']}


if __name__ == '__main__':
    result = validate()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(1 if result['failures'] else 0)
