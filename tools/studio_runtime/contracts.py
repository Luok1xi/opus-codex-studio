"""Validate owner configuration and model-produced plans at separate boundaries."""
import json
import math
import re
from pathlib import Path

ID = re.compile(r'^[a-zA-Z0-9_-]{1,64}$')
DEFAULTS = {'max_parallel': 3, 'max_calls': 16, 'max_repairs': 1,
            'timeout_seconds': 900, 'quota_ttl_seconds': 60, 'reserve_percent': 5,
            'context_chars': 16000, 'max_tasks': 12, 'max_recoveries': 2}


def load_config(path):
    config = json.loads(Path(path).read_text('utf-8-sig'))
    if not isinstance(config, dict) or config.get('version') != 1 or not isinstance(config.get('agents'), dict):
        raise ValueError('Expected version 1 and agents object')
    if not isinstance(config.get('limits', {}), dict) or not isinstance(config.get('checks', {}), dict):
        raise ValueError('limits and checks must be objects')
    config['limits'] = DEFAULTS | config.get('limits', {})
    bounds = {'max_parallel': (1, 16), 'max_calls': (1, 100), 'max_repairs': (0, 3),
              'timeout_seconds': (1, 7200), 'quota_ttl_seconds': (1, 300),
              'reserve_percent': (0, 50), 'context_chars': (4000, 64000), 'max_tasks': (1, 50),
              'max_recoveries': (0, 5)}
    for key, (low, high) in bounds.items():
        if type(config['limits'][key]) is not int or not low <= config['limits'][key] <= high:
            raise ValueError('Invalid limit: ' + key)
    if not config['agents']:
        raise ValueError('Configure at least one agent')
    for name, agent in config['agents'].items():
        if not ID.fullmatch(name) or not isinstance(agent, dict):
            raise ValueError('Invalid agent')
        agent['id'] = name
        if agent.get('provider') not in ('codex', 'claude', 'deepseek', 'command'):
            raise ValueError('Unsupported provider: ' + name)
        if type(agent.get('enabled', True)) is not bool:
            raise ValueError('enabled must be boolean: ' + name)
        for field in ('model', 'quota_group'):
            if field in agent and (not isinstance(agent[field], str) or not agent[field].strip()):
                raise ValueError('Invalid ' + field + ': ' + name)
        if 'reasoning_effort' in agent and (agent['provider'] != 'codex' or
                agent['reasoning_effort'] not in ('low', 'medium', 'high', 'xhigh', 'max')):
            raise ValueError('reasoning_effort requires Codex and a supported effort name: ' + name)
        balance = agent.get('reserve_balance', 0)
        if type(balance) not in (int, float) or not math.isfinite(balance) or balance < 0:
            raise ValueError('reserve_balance must be a finite nonnegative number: ' + name)
        if not isinstance(agent.get('capabilities'), list) or not agent['capabilities'] or any(
                not isinstance(x, str) or not ID.fullmatch(x) for x in agent['capabilities']):
            raise ValueError('Agent capabilities required: ' + name)
        for field in ('command', 'probe_command'):
            if field in agent:
                validate_command(agent[field])
    for key in ('lead_order', 'worker_order'):
        if not isinstance(config.get(key), list) or not config[key] or any(
                not isinstance(x, str) or x not in config['agents'] for x in config[key]):
            raise ValueError('Invalid routing order: ' + key)
    rules = config.setdefault('routing_rules', [])
    if not isinstance(rules, list) or len(rules) > 32:
        raise ValueError('routing_rules must be a bounded list')
    for rule in rules:
        if not isinstance(rule, dict) or rule.get('role') not in ('lead', 'worker'):
            raise ValueError('Each routing rule needs a lead or worker role')
        caps, order = rule.get('capabilities'), rule.get('order')
        if not isinstance(caps, list) or not caps or any(not isinstance(x, str) or not ID.fullmatch(x) for x in caps):
            raise ValueError('Routing rule capabilities required')
        if not isinstance(order, list) or not order or any(not isinstance(x, str) or x not in config['agents'] for x in order):
            raise ValueError('Routing rule order must name registered agents')
        if not any(set(caps) <= set(config['agents'][name]['capabilities']) for name in order):
            raise ValueError('Routing rule has no capable candidate')
    config.setdefault('checks', {})
    for name, command in config['checks'].items():
        if not ID.fullmatch(name):
            raise ValueError('Invalid check name')
        validate_command(command)
    return config


def validate_command(command):
    if not isinstance(command, list) or not command or any(not isinstance(x, str) or not x or '\0' in x for x in command):
        raise ValueError('Commands must be explicit argv arrays, never shell strings')


def parse_json(text):
    text = text.strip()
    if text.startswith('```'):
        if '\n' not in text or not text.endswith('```'):
            raise ValueError('Incomplete JSON code fence')
        text = text.split('\n', 1)[1].rsplit('```', 1)[0]
    result = json.loads(text)
    if not isinstance(result, dict):
        raise ValueError('Lead response must be a JSON object')
    return result


def validate_plan(plan, config):
    tasks = plan.get('tasks') if isinstance(plan, dict) else None
    if not isinstance(tasks, list) or not 1 <= len(tasks) <= config['limits']['max_tasks']:
        raise ValueError('Plan must contain a bounded tasks array')
    ids = set()
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get('id'), str) or not ID.fullmatch(task['id']) or task['id'] in ids:
            raise ValueError('Task IDs must be unique and safe')
        ids.add(task['id'])
        if not isinstance(task.get('instruction'), str) or not 1 <= len(task['instruction']) <= 12000:
            raise ValueError('Task instruction is missing or too long')
        for key in ('depends_on', 'capabilities'):
            task.setdefault(key, [])
            if not isinstance(task[key], list) or any(not isinstance(x, str) for x in task[key]):
                raise ValueError('Invalid task ' + key)
        task.setdefault('read_only', False)
        if type(task['read_only']) is not bool:
            raise ValueError('read_only must be boolean')
        if 'agent' in task and (not isinstance(task['agent'], str) or task['agent'] not in config['agents']):
            raise ValueError('Unknown agent')
        if not any(set(task['capabilities']) <= set(agent['capabilities']) for agent in config['agents'].values()):
            raise ValueError('No configured agent supports the task capabilities')
    remaining = {task['id']: set(task['depends_on']) for task in tasks}
    if any(not deps <= ids for deps in remaining.values()):
        raise ValueError('Missing dependency')
    resolved = set()
    while remaining:
        ready = [name for name, deps in remaining.items() if deps <= resolved]
        if not ready:
            raise ValueError('Dependency cycle')
        for name in ready:
            resolved.add(name)
            del remaining[name]
    # Runtime state and native session IDs are never accepted from a model-authored plan.
    fields = ('id', 'instruction', 'depends_on', 'capabilities', 'read_only', 'agent')
    return [{key: task[key] for key in fields if key in task} for task in tasks]
