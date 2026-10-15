#!/usr/bin/env python3
"""Independent acceptance audit. Exits nonzero unless radar is usable."""
import argparse
import datetime as dt
import json
import math
from pathlib import Path

UTC = dt.timezone.utc

def check(path, now=None):
    now = now or dt.datetime.now(UTC)
    issues = []
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["Cannot load JSON: " + str(exc)]
    fixed, live = data.get("fixed"), data.get("live")
    if not isinstance(fixed, list) or not isinstance(live, list):
        return ["fixed and live must be arrays"]
    for key, rows in (("fixed_count", fixed), ("live_count", live)):
        if data.get(key) != len(rows):
            issues.append(f"{key} mismatch")
    giants = sum(row.get("giant") is True for row in live if isinstance(row, dict))
    if data.get("live_giant_count") != giants:
        issues.append("live_giant_count mismatch")
    for kind, rows in (("fixed", fixed), ("live", live)):
        seen = set()
        for i, row in enumerate(rows):
            loc = f"{kind}[{i}]"
            if not isinstance(row, dict):
                issues.append(f"{loc}: not an object")
                continue
            try:
                lat, lon = float(row["lat"]), float(row["lon"])
                if not (math.isfinite(lat) and math.isfinite(lon) and -90 <= lat <= 90 and -180 <= lon <= 180):
                    raise ValueError("out-of-range or non-finite coordinates")
                key = (round(lat, 5), round(lon, 5), row.get("name", "").casefold())
                if key in seen:
                    issues.append(f"{loc}: duplicate")
                seen.add(key)
            except (KeyError, TypeError, ValueError, AttributeError) as exc:
                issues.append(f"{loc}: invalid coordinate or name ({exc})")
            if row.get("kind") != kind:
                issues.append(f"{loc}: wrong kind")
            if kind == "fixed" and row.get("giant"):
                issues.append(f"{loc}: fixed spot cannot establish active giant")
            if kind == "live":
                try:
                    stamp = dt.datetime.fromisoformat(row["observed_at"].replace("Z", "+00:00"))
                    if stamp.tzinfo is None or not 0 <= (now - stamp).total_seconds() <= 90*60:
                        raise ValueError("stale/future/unzoned observation")
                except (KeyError, AttributeError, ValueError, TypeError) as exc:
                    issues.append(f"{loc}: invalid timestamp ({exc})")
    sources = data.get("sources", {})
    if not isinstance(sources, dict) or sources.get("fixed") in (None, "not_configured"):
        issues.append("fixed source not configured")
    if not isinstance(sources, dict) or sources.get("live") in (None, "not_configured"):
        issues.append("live source not configured")
    if not fixed:
        issues.append("no real fixed mushroom spots")
    if not live:
        issues.append("no recent observations")
    if giants == 0:
        issues.append("no confirmed active giant mushrooms (cannot validate giant display)")
    return issues

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", nargs="?", default="data/mushrooms.json")
    args = parser.parse_args()
    issues = check(args.json_file)
    print("ACCEPTANCE: PASS" if not issues else "ACCEPTANCE: FAIL")
    for issue in issues:
        print(" -", issue)
    raise SystemExit(1 if issues else 0)
