import datetime as dt
import json
import unittest
from pathlib import Path
from radar import assemble, UTC

class HistoricalPublicationTests(unittest.TestCase):
    def setUp(self):
        self.rows=json.loads(Path("data/observations_archive.json").read_text(encoding="utf-8"))["observations"]

    def test_consented_records_have_traceable_sources_and_no_extra_private_fields(self):
        allowed={"id","name","lat","lon","size","size_label","mushroom_type","kind","status","giant","observed_at","time_precision","source_url","verification","publication_consent"}
        self.assertEqual(len(self.rows),2)
        for row in self.rows:
            self.assertTrue(row["publication_consent"])
            self.assertEqual(set(row),allowed)
            self.assertTrue(row["source_url"].startswith("https://github.com/LouisChung009/pikmin-mushroom-radar/issues/"))

    def test_confirmed_sizes_coordinates_and_minute_precision_are_preserved(self):
        by_name={row["name"]:row for row in self.rows}
        red=by_name["愛的彩色電視盒"]
        crystal=by_name["愛心框框藝術"]
        self.assertEqual((red["lat"],red["lon"],red["size"]),(24.083716,120.694392,"large"))
        self.assertEqual((crystal["lat"],crystal["lon"],crystal["size"]),(24.084849,120.693019,"normal"))
        self.assertTrue(all(row["time_precision"]=="minute" for row in self.rows))
        self.assertTrue(all(row["giant"] is False for row in self.rows))

    def test_expired_publications_cannot_become_live_or_giant(self):
        now=dt.datetime(2026,10,29,14,43,tzinfo=UTC)
        output=assemble([],self.rows,now)
        self.assertEqual(output["live_count"],0)
        self.assertEqual(output["live_giant_count"],0)
        self.assertTrue(all(row["kind"]=="history" and row["status"]=="expired" for row in self.rows))

if __name__=="__main__":
    unittest.main()
