"""Pikmin Bloom mushroom radar: verified locations and time-bounded observations.

Sources must be explicitly permitted public HTTPS JSON endpoints. No Niantic
private interfaces, account credentials, or synthetic sightings are used.
"""
import datetime as dt
import json
import os
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen, Request

UTC = dt.timezone.utc
GIANT = {"giant", "巨大", "giant mushroom", "巨型", "巨大蘑菇"}
MAX_BYTES = 5_000_000
MAX_ITEMS = 20_000
OUT = Path("data/mushrooms.json")

def fetch(url):
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Only public HTTPS sources without URL credentials are supported")
    req = Request(url, headers={"User-Agent": "PikminMushroomRadar/1.1"})
    with urlopen(req, timeout=20) as response:
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("Feed exceeds 5 MB")
    payload = json.loads(raw)
    rows = payload if isinstance(payload, list) else payload.get("mushrooms", [])
    if not isinstance(rows, list):
        raise ValueError("Feed must contain a mushrooms array")
    return rows[:MAX_ITEMS], parsed.hostname

def coords(item):
    lat = float(item["lat"])
    lon = float(item.get("lon", item.get("lng")))
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise ValueError("Invalid coordinates")
    return lat, lon

def observed_time(value):
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.astimezone(UTC) if parsed.tzinfo else None
    except ValueError:
        return None

def normalize(rows, kind, now, ttl_minutes):
    result = {}
    for item in rows:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            continue
        # Community maps can mix flowers and mushrooms in the same feed.
        # Unknown or unspecified types remain admissible for dedicated
        # mushroom-only feeds; explicitly non-mushroom types are rejected.
        raw_type = str(item.get("type", "")).strip().lower()
        if raw_type and raw_type not in ("菇點", "蘑菇", "mushroom", "mushrooms", "菇", "mushroom spot"):
            continue
        try:
            lat, lon = coords(item)
        except (TypeError, ValueError, KeyError):
            continue
        size = str(item.get("size", "")).strip().lower()
        when = observed_time(item.get("observed_at"))
        if kind == "live":
            # A live mushroom is only valid when explicitly observed recently.
            if when is None or not (dt.timedelta(0) <= now - when <= dt.timedelta(minutes=ttl_minutes)):
                continue
        name = item["name"].strip()[:160]
        if not name:
            continue
        entry = {"name": name, "lat": lat, "lon": lon, "size": size,
                 "giant": size in GIANT, "kind": kind,
                 "observed_at": when.isoformat() if when else None,
                 "country": str(item.get("country", ""))[:80],
                 "mushroom_type": str(item.get("mushroom_type", ""))[:80]}
        key = (round(lat, 5), round(lon, 5), name.casefold())
        prev = result.get(key)
        if prev is None or (entry["observed_at"] or "") > (prev["observed_at"] or ""):
            result[key] = entry
    return list(result.values())

def assemble(fixed_rows, live_rows, now=None, ttl_minutes=90):
    now = now or dt.datetime.now(UTC)
    if ttl_minutes < 1 or ttl_minutes > 1440:
        raise ValueError("TTL must be 1–1440 minutes")
    fixed = normalize(fixed_rows, "fixed", now, ttl_minutes)
    live = normalize(live_rows, "live", now, ttl_minutes)
    # When both feeds report the same coordinate and name, the observation
    # stays in the live layer; it never modifies the source location feed.
    fixed.sort(key=lambda x: (x["country"], x["name"]))
    live.sort(key=lambda x: (not x["giant"], x["name"]))
    return {"updated_at": now.isoformat(), "ttl_minutes": ttl_minutes,
            "fixed_count": len(fixed), "live_count": len(live),
            "live_giant_count": sum(x["giant"] for x in live),
            "fixed": fixed, "live": live}

def main():
    now = dt.datetime.now(UTC)
    ttl = int(os.getenv("OBSERVATION_TTL_MINUTES", "90"))
    fixed, live, sources, errors = [], [], {}, []
    for kind, env in (("fixed", "FIXED_SOURCE_URL"), ("live", "MUSHROOM_SOURCE_URL")):
        url = os.getenv(env, "").strip()
        if not url:
            sources[kind] = "not_configured"
            continue
        try:
            rows, hostname = fetch(url)
            if kind == "fixed":
                fixed = rows
            else:
                live = rows
            sources[kind] = hostname
        except Exception as exc:
            # Fail the job rather than publish a false empty success.
            errors.append(f"{kind}: {type(exc).__name__}: {exc}")
    if errors:
        raise RuntimeError("; ".join(errors))
    from report_ingest import approved_observations
    github_token = os.getenv("GITHUB_TOKEN", "")
    community = approved_observations(os.getenv("GITHUB_REPOSITORY", ""), github_token, now)
    live.extend(community)
    sources["community"] = "github_issues_maintainer_approved" if github_token else "not_configured"
    output = assemble(fixed, live, now, ttl)
    output["sources"] = sources
    approved_by_name = {row["name"]: row for row in community}
    for row in output["live"]:
        source_row = approved_by_name.get(row["name"])
        if source_row:
            row["source"] = source_row["source"]
            row["verification"] = source_row["verification"]
    output["status"] = "ok" if fixed or live else "no_observations"
    OUT.parent.mkdir(exist_ok=True, parents=True)
    OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"status={output['status']} fixed={output['fixed_count']} live={output['live_count']} giant={output['live_giant_count']}")
    if os.getenv("REQUIRE_LIVE_DATA") == "1" and not live:
        raise RuntimeError("Live data required but source returned zero rows")

if __name__ == "__main__":
    main()
