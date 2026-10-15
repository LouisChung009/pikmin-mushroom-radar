import datetime as dt
import unittest
from gemini_discovery import collect, extract_grounding, sanitize_url

class GeminiDiscoveryTests(unittest.TestCase):
    def test_only_grounded_links(self):
        payload = {"candidates":[{"content":{"parts":[{"text":"Invented coordinates 1,2"}]},
            "groundingMetadata":{"groundingChunks":[
                {"web":{"uri":"https://example.org/a","title":"Report"}},
                {"web":{"uri":"https://example.org/a","title":"Duplicate"}},
                {"web":{"uri":"javascript:alert(1)","title":"Unsafe"}}]}}]}
        result = extract_grounding(payload)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["verification"],"unverified_search_result")
        self.assertNotIn("lat",result[0])
        self.assertNotIn("lon",result[0])

    def test_missing_grounding_yields_no_results(self):
        self.assertEqual(extract_grounding({"candidates":[{"content":{"parts":[{"text":"giant near Taipei"}]}}]}), [])

    def test_search_deduplication(self):
        def fake(*args):
            return {"candidates":[{"groundingMetadata":{"groundingChunks":[
                {"web":{"uri":"https://example.org/post","title":"Post"}}]}}]}
        now = dt.datetime(2026,10,15,tzinfo=dt.timezone.utc)
        result=collect("fake","fake",["one","two"],now,request_fn=fake)
        self.assertEqual(result["count"],1)
        self.assertEqual(result["queries"],2)
        self.assertEqual(result["mode"],"leads_only_not_verified_game_locations")

    def test_bad_urls(self):
        self.assertIsNone(sanitize_url("file:///etc/passwd"))
        self.assertIsNone(sanitize_url("https://user:pass@example.com"))
        self.assertIsNone(sanitize_url(""))
if __name__=="__main__":
    unittest.main()
