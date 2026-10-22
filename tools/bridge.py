"""Portable entry point: python tools/bridge.py --help. No import-time inference."""
import argparse
import json
import signal
import sys
from pathlib import Path

from studio_runtime.contracts import load_config, validate_plan
from studio_runtime.store import Store


def main():
    parser = argparse.ArgumentParser(description='通用本地 AI 协作桥：主脑、成员、任务与成果分离')
    parser.add_argument('--config', default='bridge.local.json', help='Owner-controlled agent/check configuration')
    parser.add_argument('--state', default='.studio-runtime', help='Local queue and evidence, never committed')
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('doctor', help='Read installed clients and available quotas; no model inference')
    consult = sub.add_parser('consult', help='Call DeepSeek once and persist its answer/session; no automatic retry or quota claim')
    consult.add_argument('--prompt-file', required=True)
    consult.add_argument('--workspace', required=True)
    consult.add_argument('--connection', default=str(Path(__file__).resolve().parents[1] / '.studio-runtime/deepseek-connection.json'))
    consult.add_argument('--session')
    consult.add_argument('--timeout', type=int, default=120, choices=range(1, 901), metavar='1..900')
    consult.add_argument('--key', required=True, help='Reuse the same key after a lost reply to retrieve the saved job')
    submit = sub.add_parser('submit', help='Queue a goal for any workspace')
    submit.add_argument('--workspace', required=True)
    submit.add_argument('--goal-file', required=True)
    submit.add_argument('--plan', help='Optional owner-written task graph; otherwise the lead creates it')
    submit.add_argument('--priority', type=int, default=50)
    submit.add_argument('--key', help='Idempotency key: repeat submissions return the same job')
    run = sub.add_parser('run', help='Run queued work using authenticated clients')
    run.add_argument('--watch', action='store_true', help='Wait for new jobs without idle model calls')
    status = sub.add_parser('status')
    status.add_argument('job', nargs='?')
    events = sub.add_parser('events', help='Incremental event cursor; does not reload full transcripts')
    events.add_argument('job')
    events.add_argument('--after', type=int, default=0)
    sub.add_parser('stop', help='Cancel owned processes and preserve checkpoints')
    args = parser.parse_args()
    store = Store(args.state)
    if args.action == 'consult':
        from deepseek_task import ask
        from studio_runtime.consult import consult
        result = consult(store, ask, workspace=str(Path(args.workspace).resolve(strict=True)),
                         prompt=Path(args.prompt_file).read_text('utf-8-sig'), connection=Path(args.connection).resolve(strict=True),
                         session=args.session, timeout=args.timeout, key=args.key)
    elif args.action == 'status':
        result = store.get(args.job) if args.job else [{k: x.get(k) for k in (
            'id', 'workspace', 'status', 'phase', 'lead', 'calls', 'metrics', 'review')} for x in store.list()]
    elif args.action == 'events':
        result = store.events(args.job, args.after)
    elif args.action == 'stop':
        (store.root / 'stop.request').write_text('stop', encoding='utf-8')
        result = {'stop_requested': True}
    else:
        config = load_config(args.config)
        if args.action == 'submit':
            plan = validate_plan(json.loads(Path(args.plan).read_text('utf-8-sig')), config) if args.plan else None
            result = store.submit(args.workspace, Path(args.goal_file).read_text('utf-8-sig'), args.priority, args.key, plan)
        else:
            from studio_runtime.adapters import Providers, run_command
            from studio_runtime.engine import Bridge
            bridge = Bridge(store, config, Providers(), run_command)
            if args.action == 'doctor':
                result = {name: bridge.router.health(name) for name in config['agents']}
            else:
                signal.signal(signal.SIGINT, lambda *_: bridge.cancel.set())
                signal.signal(signal.SIGTERM, lambda *_: bridge.cancel.set())
                bridge.run(args.watch)
                result = [{k: job.get(k) for k in ('id', 'status', 'lead', 'calls', 'review')} for job in store.list()]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if args.action == 'consult' and result['status'] != 'answered' else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
