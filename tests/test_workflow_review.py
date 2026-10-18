import copy
import unittest
from tools.workflow_review import analyse, render


def record():
    return dict(schema_version=1, round_id='2026-10-18-test', task_summary='test',
                workflow_version='v1', started_at='2026-10-18T00:00:00Z',
                measurement_cutoff_at='2026-10-18T00:01:00Z',
                quality=dict(status='passed', acceptance=['check'], completed=['check'], remaining=[]),
                metrics=[dict(name='usage', value=None, unit='tokens', basis='not reported')],
                observations=[], recommendations=[], evidence=['test receipt'], comparison=None, limits=['one case'])


class ReviewTests(unittest.TestCase):
    def test_no_baseline_never_invents_savings(self):
        data = record()
        self.assertEqual(analyse(data)['wall_seconds'], 60)
        self.assertIsNone(analyse(data)['observed_time_change_pct'])
        self.assertIn('未知', render(data))
        data['metrics'][0]['value'] = 0
        self.assertIn('| 0 | tokens |', render(data))

    def test_only_matching_quality_gated_pair_has_observed_delta(self):
        data = record()
        keys = dict(task_fingerprint='a', acceptance_fingerprint='b', environment_fingerprint='c', protocol_id='p1')
        data['comparison'] = dict(current=keys, baseline=dict(keys, wall_seconds=120, quality_status='passed', evidence='baseline'))
        self.assertEqual(analyse(data)['observed_time_change_pct'], 50)
        for section, key, value in [('quality', 'status', 'partial'), ('current', 'task_fingerprint', 'changed'), ('baseline', 'quality_status', 'failed')]:
            changed = copy.deepcopy(data)
            target = changed['quality'] if section == 'quality' else changed['comparison'][section]
            target[key] = value
            self.assertIsNone(analyse(changed)['observed_time_change_pct'])
        data['comparison']['baseline']['wall_seconds'] = 30
        self.assertEqual(analyse(data)['observed_time_change_pct'], -100)

    def test_bad_time_and_nonfinite_metrics_fail(self):
        for field, value in [('started_at', '2026-10-19T00:00:00Z'), ('started_at', '2026-10-18T00:00:00')]:
            data = record()
            data[field] = value
            with self.assertRaises(ValueError):
                analyse(data)
        for value in (float('nan'), float('inf'), -1, True):
            data = record()
            data['metrics'][0]['value'] = value
            with self.assertRaises(ValueError):
                analyse(data)

    def test_missing_evidence_or_false_pass_rejected(self):
        data = record()
        data['evidence'] = []
        with self.assertRaises(ValueError):
            analyse(data)
        data = record()
        data['quality']['remaining'] = ['unfinished']
        with self.assertRaises(ValueError):
            analyse(data)


if __name__ == '__main__':
    unittest.main()
