# Pikmin Mushroom Radar

Global Pikmin Bloom mushroom location **framework** with separate fixed locations and time-sensitive observations. No live worldwide coverage is claimed without a verified observation source.

## Automatic refresh
GitHub Actions: `.github/workflows/radar.yml`. Scheduled at minute 7 and 37 of every hour (GitHub best effort), plus manual `workflow_dispatch`. Six acceptance tests run before collection; results are committed to `data/mushrooms.json`.

## Data sources (GitHub Actions repository secrets)
- `FIXED_SOURCE_URL`: authorized publicly accessible HTTPS JSON feed of *known locations*. These are NOT current mushroom spawns.
- `MUSHROOM_SOURCE_URL`: authorized HTTPS JSON feed of *observations* with accurate `observed_at` timestamp.
- Optional `OBSERVATION_TTL_MINUTES` defaults to 90 (currently configured in workflow).

Format: a JSON array or `{"mushrooms": [...]}`. Each record needs `name`, `lat`, `lon` (or `lng`); live records additionally require `observed_at` as timezone-aware ISO 8601 and `size`. Values `giant`, `巨大`, `giant mushroom`, `巨型`, `巨大蘑菇` count as giant.

`data/mushrooms.json` contains `fixed`, `live`, counts, sources, status, and a timestamp. Missing sources produce explicit `no_observations` status. Source failures fail the workflow rather than silently replacing them with empty data.

## Test locally
```sh
python -m unittest discover -s tests -v
python radar.py
```

## Verified candidate sources (not connected by default)
- https://github.com/LIUXVuse/pikmin-bloom-map — community-reported GPS points; redistribution/automated use permission must be verified.
- https://github.com/odyliao-lab/pikmin-mush — scanner uses rooted Android devices and version-specific hooks, **not** a documented public realtime JSON API.
- https://github.com/Tr6nt0/bloom-scout-plugin — map tooling, not a guaranteed live observation feed.

No private game API calls, login/session scraping, or invented positions. Existing ChatGPT site at `pikmin-mushroom-finder.perkyzebra10.chatgpt.site` is **not** automatically connected to this private repository. To connect it, an authenticated backend/proxy or an intentionally published safe data endpoint will be necessary. Never embed a private GitHub token into browser JavaScript.
