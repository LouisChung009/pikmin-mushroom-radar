"""Collect public, explicitly supplied Pikmin Bloom mushroom observations.

Set MUSHROOM_SOURCE_URL to a permitted HTTPS JSON feed. No game API is
assumed, no authentication is bypassed, and no locations are invented.
"""
import datetime as dt
import json
import os
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

OUTPUT = Path("data/mushrooms.json")
SOURCE = os.environ.get("MUSHROOM_SOURCE_URL", "").strip()
NOW = dt.datetime.now(dt.timezone.utc).isoformat()
MAX_ITEMS = 20000

def valid(row):
    if not isinstance(row, dict):
        return False
    try:
        lat, lon = float(row["lat"]), float(row["lon"])
    except (ValueError, TypeError, KeyError):
        return False
    return -90 <= lat <= 90 and -180 <= lon <= 180 and isinstance(row.get("name"), str)

def main():
    output = {"updated_at": NOW, "status": "source_not_configured",
              "source": None, "count": 0, "giant_count": 0, "mushrooms": []}
    if SOURCE:
        parsed = urlparse(SOURCE)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("Source must be a public HTTPS URL without credentials")
        req = Request(SOURCE, headers={"User-Agent": "PikminMushroomRadar/1.0"})
        with urlopen(req, timeout=20) as response:
            if int(response.headers.get("Content-Length", "0")) > 5_000_000:
                raise ValueError("Feed too large")
            raw = response.read(5_000_001)
        if len(raw) > 5_000_000:
            raise ValueError("Feed too large")
        data = json.loads(raw)
        rows = data if isinstance(data, list) else data.get("mushrooms", [])
        if not isinstance(rows, list):
            raise ValueError("Expected list or object with mushrooms list")
        seen = set()
        items = []
        for row in rows[:MAX_ITEMS]:
            if not valid(row):
                continue
            size = str(row.get("size", "")).lower()
            key = (round(float(row["lat"]), 5), round(float(row["lon"]), 5),
                   row["name"].strip(), size)
            if key in seen:
                continue
            seen.add(key)
            items.append({"name": row["name"][:160], "lat": float(row["lat"]),
                          "lon": float(row["lon"]), "size": size,
                          "observed_at": str(row.get("observed_at", ""))[:40]})
        items.sort(key=lambda x: x["size"] not in ("giant", "巨大", "giant mushroom"))
        output.update(status="ok", source=parsed.hostname, count=len(items),
                      giant_count=sum(x["size"] in ("giant", "巨大", "giant mushroom") for x in items),
                      mushrooms=items)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"status={output['status']} count={output['count']} giant={output['giant_count']}")

if __name__ == "__main__":
    main()
