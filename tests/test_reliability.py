import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import radar
from audit_acceptance import check

NOW = dt.datetime(2026, 10, 23, 6, tzinfo=radar.UTC)

class ReliabilityTests(unittest.TestCase):
    def test_fixed_size_never_establishes_active_giant(self):
        result = radar.assemble([{"name":"spot","lat":25,"lon":121,"size":"giant"}], [], NOW)
        self.assertFalse(result["fixed"][0]["giant"])

    def test_provenance_belongs_to_each_row_not_same_name(self):
        rows = [{"name":"same","lat":25,"lon":121,"size":"giant",
                 "observed_at":NOW.isoformat(),"source_url":"https://example.org/1"},
                {"name":"same","lat":26,"lon":121,"size":"normal",
                 "observed_at":NOW.isoformat(),"source_url":"https://example.org/2"}]
        self.assertEqual({x["source_url"] for x in radar.assemble([],rows,NOW)["live"]},
                         {"https://example.org/1","https://example.org/2"})

    def test_unchanged_data_does_not_republish_timestamp(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"mushrooms.json"
            first = radar.assemble([], [], NOW)
            self.assertTrue(radar.publish(first,path))
            second = radar.assemble([], [], NOW+dt.timedelta(minutes=30))
            self.assertFalse(radar.publish(second,path))
            self.assertEqual(json.loads(path.read_text())["updated_at"],NOW.isoformat())

    def test_raw_stale_rows_cannot_satisfy_required_live_data(self):
        old = [{"name":"stale","lat":25,"lon":121,"observed_at":"2020-01-01T00:00:00Z"}]
        with tempfile.TemporaryDirectory() as folder, patch.dict("os.environ",
                {"MUSHROOM_SOURCE_URL":"https://example.org/feed",
                 "MUSHROOM_SOURCE_LICENSE_URL":"https://example.org/license",
                 "FIXED_SOURCE_URL":"","GITHUB_TOKEN":"","REQUIRE_LIVE_DATA":"1"}):
            with patch.object(radar,"fetch",return_value=(old,"example.org")), patch.object(radar,"OUT",Path(folder)/"m.json"):
                with self.assertRaisesRegex(RuntimeError,"zero rows"):
                    radar.main()

    def test_audit_reports_non_object_payload_without_crashing(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"m.json"
            path.write_text("[]")
            self.assertTrue(check(path,NOW))

    def test_missing_feed_license_stops_collection(self):
        with patch.dict("os.environ",{"MUSHROOM_SOURCE_URL":"https://example.org/feed",
                "MUSHROOM_SOURCE_LICENSE_URL":"","FIXED_SOURCE_URL":""}):
            with self.assertRaisesRegex(RuntimeError,"license"):
                radar.main()
