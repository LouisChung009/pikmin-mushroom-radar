# Pikmin Mushroom Radar

GitHub Actions schedules a refresh every 30 minutes (best effort; GitHub may delay runs).

## Configure data source
In Settings → Secrets and variables → Actions, add repository secret `MUSHROOM_SOURCE_URL` containing an authorized public HTTPS JSON feed URL.

Accepted JSON: an array of records, or an object with a `mushrooms` array. Each record requires `name`, `lat`, `lon`, `size`; optional `observed_at`. Giant values: `giant`, `巨大`, `giant mushroom`.

Run the workflow manually in the Actions tab to test. Results appear in `data/mushrooms.json`. If no source is configured, the output explicitly reports `source_not_configured`, rather than inventing mushroom sightings.

This does not access private Niantic APIs or guarantee worldwide live coverage. The existing website requires separate integration.
