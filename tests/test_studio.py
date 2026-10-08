import json
from pathlib import Path
import shutil
import tempfile
import unittest
from tools.studio_check import ROOT, validate


class PackageChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='studio-test-', dir=ROOT.parent)
        self.root = Path(self.tmp.name)/'studio'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__', '.git'))

    def tearDown(self):
        self.tmp.cleanup()

    def test_current_package_passes(self):
        self.assertEqual(validate(self.root)['status'], 'PASS')

    def test_missing_entry_is_detected(self):
        (self.root/'AGENTS.md').unlink()
        self.assertIn('missing: AGENTS.md', validate(self.root)['failures'])

    def test_vendor_tamper_is_detected(self):
        path = self.root/'studio/vendor/ccgs/LICENSE'
        path.write_text('changed', encoding='utf-8')
        self.assertTrue(any('vendor hash mismatch' in f for f in validate(self.root)['failures']))

    def test_lock_cannot_escape_package(self):
        path = self.root/'studio/upstream.lock.json'
        data = json.loads(path.read_text('utf-8'))
        data['files'][0]['installed'] = '../outside'
        path.write_text(json.dumps(data), encoding='utf-8')
        self.assertTrue(any('path outside package' in f for f in validate(self.root)['failures']))

    def test_automation_must_stay_explicit(self):
        path = self.root/'studio.config.json'
        cfg = json.loads(path.read_text('utf-8'))
        cfg['automatic_model_calls'] = True
        path.write_text(json.dumps(cfg), encoding='utf-8')
        self.assertIn('unexpected automation: automatic_model_calls', validate(self.root)['failures'])


if __name__ == '__main__':
    unittest.main()
