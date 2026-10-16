"""Import maintainer-approved, consented community observations from GitHub Issues."""
import datetime as dt
import json
import os
import re
from urllib.request import Request, urlopen\nfrom urllib.error import HTTPError
from urllib.parse import urlencode

UTC = dt.timezone.utc
APPROVED_LABEL = "radar-approved"
MAX_ISSUES = 1000

def _field(body, *names):
    lines = body.splitlines()
    aliases = {name.casefold() for name in names}
    for i, line in enumerate(lines):
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if heading and heading.group(1).strip().casefold() in aliases:
            for candidate in lines[i + 1:]:
                value = candidate.strip()
                if value and not value.startswith("#"):
                    return value
    return ""

def _checked(value):
    return bool(re.search(r"(?im)^\s*-\s*\[x\]\s+.+$", value))

def parse_issue(issue, now=None):
    now = now or dt.datetime.now(UTC)
    body = issue.get("body") or ""
    # Require explicit personal observation and public-coordinate consent.
    if not _checked(_field(body, "本人親眼觀測", "親眼觀測")):
        return None
    if not _checked(_field(body, "同意公開精確座標", "公開同意")):
        return None
    stamp = _field(body, "觀測時間（UTC）", "觀測時間 (UTC)", "觀測時間")
    try:
        observed = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        if observed.tzinfo is None:
            return None
        observed = observed.astimezone(UTC)
    except (ValueError, TypeError):
        return None
    if not dt.timedelta(0) <= now - observed <= dt.timedelta(minutes=90):
        return None
    try:
        lat = float(_field(body, "緯度"))
        lon = float(_field(body, "經度", "longitude"))
    except ValueError:
        return None
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    size = _field(body, "大小", "蘑菇大小").strip().casefold()
    if size not in {"small", "normal", "large", "giant", "小", "普通", "大", "巨大"}:
        return None
    mushroom_type = _field(body, "種類", "蘑菇種類", "顏色")[:80]
    name = "社群回報 #" + str(issue.get("number", ""))
    return {
        "name": name, "lat": lat, "lon": lon, "size": size,
        "type": "mushroom", "observed_at": observed.isoformat(),
        "source": "community_issue", "verification": "maintainer_approved_report",
        "mushroom_type": mushroom_type
    }

def ensure_approval_label(repo, token):
    """Create the moderation label once if it is missing."""
    if not repo or not token:
        return
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "PikminMushroomRadar/1.0",
    }
    label_url = f"https://api.github.com/repos/{repo}/labels/{APPROVED_LABEL}"
    try:
        with urlopen(Request(label_url, headers=headers), timeout=20):
            return
    except HTTPError as exc:
        if exc.code != 404:
            raise
    payload = json.dumps({
        "name": APPROVED_LABEL,
        "color": "1f6feb",
        "description": "Maintainer-approved public mushroom observations",
    }).encode("utf-8")
    create = Request(
        f"https://api.github.com/repos/{repo}/labels",
        data=payload,
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(create, timeout=20):
        return

def approved_observations(repo, token, now=None):
    if not token:
        return []
    rows, page = [], 1
    while page <= 10 and len(rows) < MAX_ISSUES:
        query = urlencode({"state": "all", "labels": APPROVED_LABEL, "per_page": 100, "page": page})
        req = Request(f"https://api.github.com/repos/{repo}/issues?{query}", headers={
            "Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "PikminMushroomRadar/1.0"})
        with urlopen(req, timeout=20) as response:
            items = json.loads(response.read(2_000_001))
        if not isinstance(items, list):
            raise ValueError("GitHub Issues API returned an unexpected payload")
        if not items:
            break
        for issue in items:
            if "pull_request" in issue:
                continue
            labels = {item.get("name") for item in issue.get("labels", [])}
            if APPROVED_LABEL not in labels:
                continue
            record = parse_issue(issue, now)
            if record:
                rows.append(record)
        if len(items) < 100:
            break
        page += 1
    return rows[:MAX_ISSUES]

def main():
    repo = os.getenv("GITHUB_REPOSITORY", "")
    records = approved_observations(repo, os.getenv("GITHUB_TOKEN", ""))
    print(f"approved_recent_community_reports={len(records)}")
    return records

if __name__ == "__main__":
    main()
