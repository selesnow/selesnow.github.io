"""The clone API has an overlapping 14-day window; daily snapshots must not double-count it."""
import unittest
from acpgram_stats import merge_clones


class CloneHistoryTest(unittest.TestCase):
    def test_overlapping_window_replaces_days_and_keeps_older_history(self):
        old = {'history': [{'date': '2026-10-01', 'count': 3, 'uniques': 2},
                           {'date': '2026-10-14', 'count': 2, 'uniques': 1}]}
        payload = {'count': 9, 'uniques': 4, 'clones': [
            {'timestamp': '2026-10-14T00:00:00Z', 'count': 5, 'uniques': 3},
            {'timestamp': '2026-10-15T00:00:00Z', 'count': 4, 'uniques': 2}]}
        result = merge_clones(old, payload)
        self.assertEqual(result['total'], 12)
        self.assertEqual(result['since'], '2026-10-01')
        self.assertEqual(result['last14d'], 9)
        self.assertEqual(merge_clones(result, payload), result)


if __name__ == '__main__':
    unittest.main()
