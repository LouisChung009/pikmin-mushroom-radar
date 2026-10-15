"""Gemini grounded web discovery. Search leads are NOT game observations.

Requires GEMINI_API_KEY. No secret or response text is published; only
grounded URLs and page titles are saved for human verification.
"""
import datetime as dt
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from urllib.parse import urlparse

OUT = Path("data/search_sources.json")
QUERIES = [
    "Pikmin Bloom giant mushroom sightings today locations 巨大蘑菇",
    "Pikmin Bloom 巨大菇 目前 地點 座標 回報",
    "Pikmin Bloom 巨大キノコ 現在 場所",
]
MAX_LINKS = 40

def sanitize_url(url):
    if not isinstance(url, str):
        return None
    try:
        parsed = urlparse(url)
    except ValueError:
        return None
    if parsed.scheme not in ("https", "http") or not parsed.hostname or parsed.username or parsed.password:
        return None
    # Grounding citations often provide a Google redirect; preserve it
    # verbatim rather than claiming it is a direct first-party observation.
    return url[:2048]

def extract_grounding(response):
    """Collect only structured grounded citations, never free-form claims."""
    output = []
    seen = set()
    for candidate in response.get("candidates", []):
        for chunk in candidate.get("groundingMetadata", {}).get("groundingChunks", []):
            web = chunk.get("web") or {}
            uri = sanitize_url(web.get("uri"))
            if not uri or uri in seen:
                continue
            seen.add(uri)
            output.append({"title": str(web.get("title") or "Untitled")[:180],
                           "url": uri, "verification": "unverified_search_result",
                           "kind": "search_lead"})
    return output[:MAX_LINKS]

def call_gemini(key, model, query):
    endpoint = ("https://generativelanguage.googleapis.com/v1beta/models/"
                + quote(model, safe=".-") + ":generateContent")
    payload = {
        "contents": [{"parts": [{"text":
            "Search the public web for recent Pikmin Bloom giant mushroom sighting reports. "
            "Find original URLs and their date, but do not invent coordinates, times or game status. "
            "Query: " + query}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {"temperature": 0.1},
    }
    req = Request(endpoint, data=json.dumps(payload).encode("utf-8"),
                  headers={"Content-Type": "application/json", "x-goog-api-key": key},
                  method="POST")
    with urlopen(req, timeout=70) as response:
        raw = response.read(1_500_001)
    if len(raw) > 1_500_000:
        raise ValueError("Gemini response exceeded size limit")
    return json.loads(raw)

def collect(key, model, queries=QUERIES, now=None, request_fn=call_gemini):
    now = now or dt.datetime.now(dt.timezone.utc)
    all_links = {}
    for query in queries:
        response = request_fn(key, model, query)
        for row in extract_grounding(response):
            all_links[row["url"]] = row
    return {"searched_at": now.isoformat(), "source": "gemini_google_search_grounding",
            "mode": "leads_only_not_verified_game_locations",
            "queries": len(queries), "count": len(all_links),
            "results": list(all_links.values())[:MAX_LINKS]}

def main():
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()
    if not key:
        # Explicitly indicate not configured; never fabricate web results.
        data = {"searched_at": None, "source": "gemini_google_search_grounding",
                "mode": "not_configured", "queries": 0, "count": 0, "results": []}
    else:
        data = collect(key, model)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Gemini search leads: " + str(data["count"]) + "; mode: " + data["mode"])

if __name__ == "__main__":
    main()
