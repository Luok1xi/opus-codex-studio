import ast
import copy
import json
from pathlib import Path
import unittest
from tools.task_route import route_task
from tools.studio_check import validate

ROOT = Path(__file__).resolve().parents[1]


class StudioBudgetTests(unittest.TestCase):
    def test_green_is_codex_only(self):
        result = route_task('GREEN')
        self.assertEqual(result['participants'], ['codex'])
        self.assertEqual(result['automatic_model_calls'], 0)

    def test_yellow_has_no_codex_review(self):
        self.assertEqual(route_task('YELLOW')['participants'], ['claude'])

    def test_red_stops_at_two_rounds_and_later(self):
        self.assertEqual(route_task('RED', 1)['remaining_rounds'], 1)
        for rounds in [2, 3, 100]:
            result = route_task('RED', rounds)
            self.assertEqual(result['state'], 'OWNER_DECISION')
            self.assertEqual(result['participants'], ['creative-owner'])

    def test_invalid_and_unsafe_configuration_fails_closed(self):
        for level, rounds in [('BLUE', 0), ('RED', -1), ('RED', True)]:
            with self.assertRaises(ValueError):
                route_task(level, rounds)
        cfg = json.loads((ROOT/'studio.config.json').read_text(encoding='utf-8'))
        for key, value in [('automatic_model_calls', True), ('max_red_rounds', 3),
                           ('routes', {'GREEN':['codex','claude']})]:
            altered = copy.deepcopy(cfg)
            altered[key] = value
            with self.assertRaises(ValueError):
                route_task('GREEN', config=altered)

    def test_project_configuration_and_vendor_hashes(self):
        self.assertEqual(validate()['failures'], [])

    def test_router_has_no_process_or_network_imports(self):
        # Scope is the small routing utility, not every possible client behavior.
        tree = ast.parse((ROOT/'tools/task_route.py').read_text(encoding='utf-8'))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module.split('.')[0])
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, ['eval','exec','__import__'])
        self.assertLessEqual(imports, {'argparse','json','pathlib'})


if __name__ == '__main__':
    unittest.main()
