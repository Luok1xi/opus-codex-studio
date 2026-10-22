"""Explicit DeepSeek headless calls using the installed official runtime."""
import argparse
import json
from pathlib import Path
import sys

if __package__:
    from .studio_runtime.adapters import run_command, _public_error
else:
    from studio_runtime.adapters import run_command, _public_error


def receipt(run):
    result = {'status': run['status'], 'session_id': None, 'text': ''}
    completed = False
    error = False
    for line in run.get('stdout', '').splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        if event.get('type') == 'session' and isinstance(event.get('sessionId'), str):
            result['session_id'] = event['sessionId']
        elif event.get('type') == 'final' and isinstance(event.get('text'), str):
            result['text'] = event['text']
        elif event.get('type') == 'status' and event.get('phase') == 'turn_end':
            reason = event.get('reason')
            completed = isinstance(reason, dict) and reason.get('kind') == 'completed'
        elif event.get('type') == 'error':
            error = True
    if run['status'] == 'succeeded' and (run.get('code') != 0 or not completed or error or not result['text'].strip()):
        result['status'] = 'failed'
    if result['status'] != 'succeeded':
        result['diagnostic'] = _public_error(run.get('stderr', ''))[-2000:] or 'No verified completed answer was received.'
    return result


def ask(connection, prompt, *, workspace=None, session=None, timeout=120):
    config = json.loads(Path(connection).read_text('utf-8-sig'))
    command = config.get('command') if isinstance(config, dict) else None
    if not isinstance(command, list) or not command or any(not isinstance(x, str) or not x or '\0' in x for x in command):
        raise ValueError('Connection command must be an explicit argv array')
    workspace = Path(workspace or config['workspace']).resolve(strict=True)
    if not workspace.is_dir() or type(timeout) is not int or not 1 <= timeout <= 900:
        raise ValueError('An existing workspace and timeout of 1–900 seconds are required')
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 32000:
        raise ValueError('Task text must be nonempty and at most 32000 characters')
    command = command + ['headless', '--json']
    if session is not None:
        if not isinstance(session, str) or not session or len(session) > 256 or session.startswith('-') or '\0' in session:
            raise ValueError('Invalid session identifier')
        command += ['--session-id', session]
    return receipt(run_command(command + ['-'], cwd=str(workspace), timeout=timeout, input_text=prompt))


def main():
    parser = argparse.ArgumentParser(description='Ask the official DeepSeek Harness runtime once; no retries.')
    parser.add_argument('--connection', default=str(Path(__file__).resolve().parents[1] / '.studio-runtime/deepseek-connection.json'))
    parser.add_argument('--workspace', help='Override the connection workspace for a new task')
    parser.add_argument('--prompt-file', required=True, help='UTF-8 task text, sent through stdin')
    parser.add_argument('--session', help='Continue the returned native session in the same workspace')
    parser.add_argument('--timeout', type=int, default=120)
    args = parser.parse_args()
    with Path(args.prompt_file).open('r', encoding='utf-8-sig') as stream:
        prompt = stream.read(32001)
    result = ask(args.connection, prompt, workspace=args.workspace, session=args.session, timeout=args.timeout)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'succeeded' else 1


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({'status': 'failed', 'diagnostic': _public_error(str(error))}, ensure_ascii=False))
        raise SystemExit(1)
