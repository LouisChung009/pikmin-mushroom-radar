import datetime as dt
import unittest
from radar import assemble, UTC

NOW = dt.datetime(2026, 10, 15, 12, 0, tzinfo=UTC)

class RadarTests(unittest.TestCase):
    def test_giant_and_sort(self):
        rows = [
            {"name":"small","lat":24.1,"lon":120.7,"size":"small","observed_at":"2026-10-15T11:55:00Z"},
            {"name":"big","lat":25,"lng":121,"size":"giant","observed_at":"2026-10-15T11:59:00Z"},
        ]
        result = assemble([], rows, NOW)
        self.assertEqual(result["live_giant_count"], 1)
        self.assertEqual(result["live"][0]["name"], "big")

    def test_stale_ignored(self):
        rows = [{"name":"old","lat":24,"lon":121,"size":"giant","observed_at":"2026-10-15T09:00:00Z"}]
        self.assertEqual(assemble([], rows, NOW)["live_count"], 0)

    def test_future_ignored(self):
        rows = [{"name":"future","lat":24,"lon":121,"size":"giant","observed_at":"2026-10-15T12:01:00Z"}]
        self.assertEqual(assemble([], rows, NOW)["live_count"], 0)

    def test_fixed_not_live(self):
        fixed = [{"name":"known spot","lat":24,"lng":121}]
        result = assemble(fixed, [], NOW)
        self.assertEqual(result["fixed_count"], 1)
        self.assertEqual(result["live_giant_count"], 0)

    def test_dedupe_and_bad_coordinates(self):
        fixed = [
            {"name":"A","lat":24,"lon":121},
            {"name":"A","lat":24,"lon":121},
            {"name":"bad","lat":999,"lon":121},
        ]
        self.assertEqual(assemble(fixed, [], NOW)["fixed_count"], 1)

    def test_observation_without_timestamp_not_live(self):
        rows = [{"name":"unknown","lat":24,"lon":121,"size":"giant"}]
        self.assertEqual(assemble([], rows, NOW)["live_count"], 0)

if __name__ == "__main__":
    unittest.main()
