"""Explicit local CLI for the shared TeamHub database; JSON output is never cell-truncated."""
import argparse
import datetime
import json
import os
from pathlib import Path
import sqlite3
import sys

from studio_runtime.teamhub import TeamHub, catalog_projects, initialize, resolve_database


def write_arguments(parser):
    parser.add_argument('--project', required=True)
    parser.add_argument('--actor', '--by', dest='actor', required=True)
    parser.add_argument('--key', required=True, help='Stable key; repeat only the same operation')


def parser_for_cli():
    parser = argparse.ArgumentParser(description='TeamHub project databases through one local catalog')
    parser.add_argument('--db', help='Existing canonical database path; init alone creates a new file')
    parser.add_argument('--config', help='Local JSON configuration containing an absolute catalog path')
    parser.add_argument('--json', action='store_true', help='Output JSON (also the default)')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init', help='Explicitly create an empty v1 database; never overwrite')
    migration = sub.add_parser('migrate', help='Upgrade with a mandatory pre-migration backup')
    migration.add_argument('--backup', required=True)
    migration.add_argument('--project')
    sub.add_parser('stats').add_argument('--project')
    sub.add_parser('projects')
    for command in ('steps', 'categories'):
        sub.add_parser(command).add_argument('project')
    query = sub.add_parser('query', help='Read-only SQL; database authorizer enforces this')
    query.add_argument('sql')
    query.add_argument('--project', help='Select one project database from the catalog')
    query.add_argument('--limit', type=int, default=200)
    get = sub.add_parser('get')
    get.add_argument('--project', required=True)
    get.add_argument('table')
    get.add_argument('id', help='Integer ID, or bvid for x_videos')
    for command in ('search', 'context'):
        read = sub.add_parser(command)
        read.add_argument('--project', required=True)
        read.add_argument('--category', help='Explicit project category code, not a legacy free-text field')
        read.add_argument('--limit', type=int, default=20)
        if command == 'search':
            read.add_argument('--text', default='')
            read.add_argument('--table')
    for command, table in (('list-findings', 'findings'), ('list-tasks', 'tasks')):
        listing = sub.add_parser(command)
        listing.add_argument('--project', required=True)
        listing.add_argument('--limit', type=int, default=200)
        listing.set_defaults(table=table)
    inbox = sub.add_parser('inbox')
    inbox.add_argument('--project', required=True)
    inbox.add_argument('--agent', required=True)
    inbox.add_argument('--limit', type=int, default=20)
    for command in ('update-task', 'ack'):
        update = sub.add_parser(command)
        write_arguments(update)
        update.add_argument('--id', type=int, required=True)
        update.add_argument('--expected-revision', '--revision', dest='revision', type=int, required=True)
        if command == 'update-task':
            update.add_argument('--status', required=True,
                                choices=('pending', 'in_progress', 'blocked', 'done', 'cancelled'))
        else:
            update.add_argument('--note', default='')
    classify = sub.add_parser('classify')
    write_arguments(classify)
    classify.add_argument('table')
    classify.add_argument('id')
    classify.add_argument('--category', required=True)
    backup = sub.add_parser('backup')
    backup.add_argument('--project')
    backup.add_argument('--to', required=True)
    export = sub.add_parser('export')
    export.add_argument('--project')
    export.add_argument('--to', help='New output folder; an existing folder is never overwritten')

    # Only these declared fields can reach the domain API.
    fields = {
        'source': ('sources', ('title', 'url'),
                   {'category': 'other', 'platform': '', 'author': '', 'published': '',
                    'reliability': 'unverified', 'status': 'collected', 'note': ''}),
        'resource': ('resources', ('url',),
                     {'kind': 'other', 'found_in': '', 'status': 'new', 'note': ''}),
        'finding': ('findings', ('topic', 'claim', 'evidence', 'source_ref'),
                    {'confidence': 'medium', 'tags': '', 'status': 'active'}),
        'param': ('params', ('category', 'item', 'value', 'source_ref'),
                  {'unit': '', 'status': 'unverified', 'note': ''}),
        'task': ('tasks', ('title', 'owner'),
                 {'description': '', 'priority': 'medium', 'status': 'pending',
                  'write_scope': '', 'blocked_by': ''}),
        'decision': ('decisions', ('title', 'decision'),
                     {'rationale': '', 'alternatives': '', 'status': 'proposed'}),
        'artifact': ('artifacts', ('name', 'path'),
                     {'type': 'file', 'version': '', 'checksum': '', 'status': 'active', 'description': ''}),
        'document': ('documents', ('title', 'path'),
                     {'owner': '', 'doc_type': '', 'summary': '', 'status': 'active'}),
        'review': ('reviews', ('target', 'result', 'notes'), {}),
        'handoff': ('handoffs', ('to_agent', 'marker'), {'path': '', 'note': ''}),
    }
    for name, (table, required, optional) in fields.items():
        addition = sub.add_parser('add-' + name, aliases=['handoff'] if name == 'handoff' else [])
        write_arguments(addition)
        addition.add_argument('--category-code', help='Explicit project category mapping')
        addition.set_defaults(table=table, value_fields=tuple(required) + tuple(optional))
        for field in required + tuple(optional):
            flag = '--' + field.replace('_', '-')
            flags = ('--ref', flag) if field == 'source_ref' else (flag,)
            addition.add_argument(*flags, dest=field, required=field in required, default=optional.get(field))
        if name == 'handoff':
            body = addition.add_mutually_exclusive_group(required=True)
            body.add_argument('--body', help='Complete handoff text')
            body.add_argument('--body-file', help='UTF-8 text file; its contents are stored in the database')
    return parser


def run(args):
    if args.command == 'projects' and not args.db and not os.environ.get('TEAMHUB_DB'):
        return catalog_projects(args.config)
    if args.command == 'init' and not args.db:
        raise ValueError('init requires an explicit --db path for a new empty project database')
    path = resolve_database(args.db, args.config, getattr(args, 'project', None))
    if args.command == 'init':
        result = initialize(path)
        return result if result is not None else {'database': str(path), 'initialized': True}
    hub = TeamHub(path)
    command = args.command
    if command == 'migrate':
        return hub.migrate(args.backup)
    if command in ('stats', 'projects'):
        return getattr(hub, command)()
    if command in ('steps', 'categories'):
        return getattr(hub, command)(args.project)
    if command == 'query':
        return hub.query(args.sql, limit=args.limit)
    if command == 'get':
        return hub.get(args.project, args.table, args.id)
    if command in ('search', 'list-findings', 'list-tasks'):
        return hub.search(args.project, category=getattr(args, 'category', None),
                          text=getattr(args, 'text', ''), table=args.table, limit=args.limit)
    if command == 'context':
        return hub.context(args.project, category=args.category, limit=args.limit)
    if command == 'inbox':
        return hub.inbox(args.project, args.agent, limit=args.limit)
    if command == 'update-task':
        return hub.update_task(args.project, args.id, args.status, args.revision, args.actor, args.key)
    if command == 'ack':
        return hub.ack(args.project, args.id, args.revision, args.actor, args.key, note=args.note)
    if command == 'classify':
        return hub.classify(args.project, args.table, args.id, args.category, args.actor, args.key)
    if command == 'backup':
        return hub.backup(args.to)
    if command == 'export':
        destination = args.to or Path(path).parent / ('db-export-' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
        return hub.export(destination)
    values = {field: getattr(args, field) for field in args.value_fields}
    actor_field = {'sources': 'collected_by', 'resources': 'found_by',
                   'decisions': 'decided_by', 'reviews': 'reviewer'}.get(args.table)
    if actor_field:
        values[actor_field] = args.actor
    if args.table == 'handoffs':
        values['body'] = Path(args.body_file).read_text('utf-8-sig') if args.body_file else args.body
    return hub.add(args.table, args.project, values, args.actor, args.key, category=args.category_code)


def main(argv=None):
    args = parser_for_cli().parse_args(argv)
    try:
        print(json.dumps(run(args), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, sqlite3.Error) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    raise SystemExit(main())
