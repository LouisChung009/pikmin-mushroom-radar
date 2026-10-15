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

## Source evaluation (2026-10-15)
- [LIUXVuse/pikmin-bloom-map](https://github.com/LIUXVuse/pikmin-bloom-map): public `spots.json`, but records mix `type: "花點"` and `type: "菇點"`. The adapter explicitly drops flower markers. Reuse/redistribution permission has **not** been established, so this dataset is **not enabled by default**. The reported 644 locations cannot be called 644 mushroom sites.
- [odyliao-lab/pikmin-mush](https://github.com/odyliao-lab/pikmin-mush): describes rooted Android scanning, but no verified public licensed real-time JSON endpoint. Not connected.
- [pixlpirate/pikmin-map](https://github.com/pixlpirate/pikmin-map): OSM-based predictions are not confirmed Pikmin mushrooms and are not ingested.

## Acceptance criteria
1. GitHub Actions workflow succeeds on the latest main commit.
2. All eight Python unit tests pass.
3. The published JSON has clear `sources`, `fixed_count`, `live_count`, `live_giant_count` fields.
4. A missing source yields `status: no_observations` and **0** live giant mushrooms, not made-up data.
5. A genuine permitted observation feed is required before claiming worldwide live coverage.
6. The separately hosted frontend is not considered integrated until it reads and displays actual JSON and the refresh timestamp.

Workflow also triggers on source-code pushes; data-only commits are ignored to avoid endless CI loops.

## Gemini Google Search grounding integration
The scheduled pipeline runs `gemini_discovery.py` to find recent *public web reports* of Pikmin Bloom giant mushrooms. This is **not** a direct Niantic game-state feed.

1. Create your Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey).
2. Add it as a GitHub Actions repository secret named **`GEMINI_API_KEY`** under Settings → Secrets and variables → Actions. **Do not paste the key into issues, code, or chat.**
3. Run **Actions → Mushroom radar refresh → Run workflow**.
4. Check `data/search_sources.json`. `mode: leads_only_not_verified_game_locations` plus nonzero `count` means grounded search links were discovered. `mode: not_configured` means the key has not been provided.
5. The frontend shows grounded citations beneath the map, visually separate from fixed or recent mushroom observations.

Safety: Gemini might find false, stale, or unrelated reports. Search citations are unverified leads, never accepted as live sightings or rendered as map markers without a separate authenticated/time-stamped data source. A successful CI run with 0 observations is not a successful end-to-end live-radar acceptance. API usage may be billed; the workflow makes three grounded requests per 30-minute run if a key is configured (~4,320 base requests per 30-day month), and individual Gemini calls can create multiple billable Google searches. Monitor Gemini usage and quotas.

Tests: `python -m unittest discover -s tests -v`, then independent live acceptance: `python audit_acceptance.py`. The latter is expected to fail until there are genuinely verified fresh observations.
