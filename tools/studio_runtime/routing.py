"""Quota probes are cached and shared; unknown is never interpreted as full."""
import threading
import time
import json


class Router:
    def __init__(self, config, providers):
        self.config = config
        self.providers = providers
        self.cache = {}
        self.blocked = {}
        self.groups = {name: agent.get('quota_group', json.dumps([agent['provider'], agent.get('model'), agent.get('command')])
                                      if agent['provider'] != 'command' else name)
                       for name, agent in config['agents'].items()}
        self.locks = {group: threading.Lock() for group in self.groups.values()}
        self.stats = {'probes': 0, 'cache_hits': 0}

    def health(self, name):
        if not self.config['agents'][name].get('enabled', True):
            return {'available': False, 'reason': 'disabled', 'windows': [], 'observed_at': time.time()}
        group = self.groups[name]
        with self.locks[group]:
            now = time.time()
            cached = self.cache.get(group)
            if cached and 0 <= now - cached.get('observed_at', 0) < self.config['limits']['quota_ttl_seconds']:
                self.stats['cache_hits'] += 1
                return cached
            agent = self.config['agents'][name]
            self.stats['probes'] += 1
            try:
                raw = self.providers.probe(agent)
                result = {key: raw[key] for key in ('available', 'reason', 'observed_at', 'windows', 'balance') if key in raw}
            except Exception:
                result = {'available': False, 'reason': 'probe-failed', 'windows': [], 'observed_at': now}
            self.cache[group] = result
            return result

    def eligible(self, name, capabilities):
        agent = self.config['agents'][name]
        if not agent.get('enabled', True) or not set(capabilities) <= set(agent['capabilities']) or self.blocked.get(name, 0) > time.time():
            return False
        row = self.health(name)
        age = time.time() - row.get('observed_at', 0)
        if not row.get('available') or not 0 <= age < self.config['limits']['quota_ttl_seconds']:
            return False
        windows = row.get('windows', [])
        if windows:
            return all(type(w.get('remaining_percent')) in (int, float)
                       and self.config['limits']['reserve_percent'] <= w['remaining_percent'] <= 100
                       and (w.get('reset_at') is None or w['reset_at'] > time.time()) for w in windows)
        balance = row.get('balance', {})
        # Currency is kept as currency; it is never converted into a subscription percentage.
        return type(balance.get('remaining')) in (int, float) and balance['remaining'] > agent.get('reserve_balance', 0)

    def select(self, role, capabilities=(), preferred=None, busy=()):
        order = self.config['lead_order' if role == 'lead' else 'worker_order']
        rule = next((rule for rule in self.config.get('routing_rules', [])
                     if rule['role'] == role and set(rule['capabilities']) <= set(capabilities)), None)
        if rule:
            # Owner-defined specialist routes take precedence over a model's preferred colleague.
            order = rule['order']
        elif preferred in order:
            order = [preferred] + [name for name in order if name != preferred]
        for name in order:
            if name not in busy and self.eligible(name, capabilities):
                return name
        return None

    def reject(self, name, reason):
        # Failure is account-wide, so parallel tasks cannot keep hammering an exhausted provider.
        until = time.time() + (3600 if reason == 'auth' else 60 if reason == 'failed' else 900)
        group = self.groups[name]
        for other, agent in self.config['agents'].items():
            if self.groups[other] == group:
                self.blocked[other] = until
                self.cache.pop(group, None)
