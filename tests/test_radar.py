import datetime as dt
import unittest
from radar import assemble, UTC
from report_ingest import parse_issue

NOW = dt.datetime(2026, 10, 16, 12, 0, tzinfo=UTC)

def issue(body, number=8):
    return {"number": number, "html_url": f"https://github.com/example/repo/issues/{number}", "body": body}

VALID_BODY = """### 觀測時間（UTC）
2026-10-16T11:55:00Z

### 緯度
25.033

### 經度
121.565

### 大小
giant

### 種類
紅色

### 本人親眼觀測
- [x] 我本人於上述時間在遊戲中看到此蘑菇，資料不是推測或 AI 搜尋結果

### 同意公開精確座標
- [x] 我同意將精確座標與觀測時間公開顯示於雷達
"""

class ReportIngestTests(unittest.TestCase):
    def test_approved_format_requires_both_consents_and_recent_time(self):
        row = parse_issue(issue(VALID_BODY), NOW)
        self.assertEqual(row["size"], "giant")
        self.assertEqual(row["verification"], "maintainer_approved_report")
        self.assertEqual(row["mushroom_type"], "紅色")

    def test_missing_consent_rejected(self):
        self.assertIsNone(parse_issue(issue(VALID_BODY.replace("- [x] 我同意", "- [ ] 我同意")), NOW))

    def test_stale_report_rejected(self):
        self.assertIsNone(parse_issue(issue(VALID_BODY.replace("11:55", "10:00")), NOW))

    def test_invalid_coordinates_rejected(self):
        self.assertIsNone(parse_issue(issue(VALID_BODY.replace("25.033", "999")), NOW))

class RadarTests(unittest.TestCase):
    def test_giant_and_sort(self):
        rows = [
            {"name":"small","lat":24.1,"lon":120.7,"size":"small","observed_at":"2026-10-16T11:55:00Z"},
            {"name":"big","lat":25,"lng":121,"size":"giant","observed_at":"2026-10-16T11:59:00Z"},
        ]
        result = assemble([], rows, NOW)
        self.assertEqual(result["live_giant_count"], 1)
        self.assertEqual(result["live"][0]["name"], "big")

    def test_stale_ignored(self):
        rows = [{"name":"old","lat":24,"lon":121,"size":"giant","observed_at":"2026-10-16T09:00:00Z"}]
        self.assertEqual(assemble([], rows, NOW)["live_count"], 0)

    def test_future_ignored(self):
        rows = [{"name":"future","lat":24,"lon":121,"size":"giant","observed_at":"2026-10-16T12:01:00Z"}]
        self.assertEqual(assemble([], rows, NOW)["live_count"], 0)

    def test_fixed_not_live(self):
        result = assemble([{"name":"known spot","lat":24,"lng":121}], [], NOW)
        self.assertEqual(result["fixed_count"], 1)
        self.assertEqual(result["live_giant_count"], 0)

    def test_dedupe_and_bad_coordinates(self):
        fixed = [{"name":"A","lat":24,"lon":121},{"name":"A","lat":24,"lon":121},{"name":"bad","lat":999,"lon":121}]
        self.assertEqual(assemble(fixed, [], NOW)["fixed_count"], 1)

    def test_mixed_community_feed_excludes_flowers(self):
        fixed = [{"name":"A mushroom","lat":24,"lng":121,"type":"菇點"},{"name":"A flower","lat":24.1,"lng":121.1,"type":"花點"},{"name":"B mushroom","lat":25,"lon":122,"type":"mushroom"}]
        result = assemble(fixed, [], NOW)
        self.assertEqual(result["fixed_count"], 2)
        self.assertEqual({r["name"] for r in result["fixed"]}, {"A mushroom", "B mushroom"})

    def test_unsupported_observation_type_rejected(self):
        rows = [{"name":"Flower","lat":24,"lon":121,"type":"flower","size":"giant","observed_at":"2026-10-16T11:59:00Z"}]
        self.assertEqual(assemble([], rows, NOW)["live_giant_count"], 0)

    def test_observation_without_timestamp_not_live(self):
        self.assertEqual(assemble([], [{"name":"unknown","lat":24,"lon":121,"size":"giant"}], NOW)["live_count"], 0)

if __name__ == "__main__":
    unittest.main()
