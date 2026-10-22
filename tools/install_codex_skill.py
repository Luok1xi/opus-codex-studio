"""Install a narrow discovery skill and a managed pointer without replacing user guidance."""
import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- ai-studio discovery -->'
END = '<!-- /ai-studio discovery -->'


def install(home, studio=ROOT, python=sys.executable):
    home, studio = Path(home).resolve(), Path(studio).resolve(strict=True)
    skill = home / 'skills/ai-studio/SKILL.md'
    target = home / 'AGENTS.md'
    override = home / 'AGENTS.override.md'
    if override.exists() and override.read_text('utf-8-sig').strip():
        raise ValueError('A global AGENTS.override.md would hide discovery; inspect it before installing.')
    source = (studio / 'skills/ai-studio/SKILL.md').read_text('utf-8')
    rendered = source.replace('@STUDIO_ROOT@', studio.as_posix()).replace('@PYTHON@', Path(python).as_posix())
    if skill.exists() and '# Local AI studio' not in skill.read_text('utf-8-sig'):
        raise ValueError('Refusing to overwrite an unrelated ai-studio skill')
    previous = target.read_text('utf-8-sig') if target.exists() else ''
    block = (START + '\nFor authorized multi-AI collaboration or DeepSeek/Opus consultation, '
             'read `' + skill.as_posix() + '`. It locates the user\'s existing generic studio and its verified CLI. '
             'This entry does not require delegation for ordinary tasks; dispatched workers must not recursively dispatch.\n' + END)
    if START in previous or END in previous:
        if previous.count(START) != 1 or previous.count(END) != 1 or previous.index(START) > previous.index(END):
            raise ValueError('Malformed studio discovery markers; preserve and inspect the existing file')
        before, rest = previous.split(START)
        _, after = rest.split(END)
        updated = before + block + after
    else:
        updated = previous + ('\n\n' if previous else '') + block + '\n'
    backup = home / 'AGENTS.before-ai-studio.md'
    if target.exists() and not backup.exists():
        backup.write_bytes(target.read_bytes())
    skill.parent.mkdir(parents=True, exist_ok=True)
    skill.write_text(rendered, encoding='utf-8')
    target.write_text(updated, encoding='utf-8')
    return skill


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-home', default=os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
    args = parser.parse_args()
    print(install(args.codex_home))
