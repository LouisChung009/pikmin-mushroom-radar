# Source verification — 2026-10-23 (Asia/Taipei)

**Production acceptance: FAIL. No permitted current giant-mushroom feed has been verified.**
This records evidence and uncertainty; public visibility does not establish redistribution permission.

| Candidate | Evidence | Permission / freshness | Decision |
| --- | --- | --- | --- |
| odyliao-lab/pikmin-mush | GitHub repository API and contents both return 404 on this check | No available license or feed contract to verify at this address | Not configured |
| bittieshsu/pikmin-mush | Public README points to the above name and mush.odyliao.cc; repository metadata has license=null; pushed_at 2026-10-06T16:01:23Z | README describes Root Android Zygisk hooks, injected game data extraction and location override. Code update time is not an observation time. No permission for this radar to republish data was verified | Do not deploy its scanner or consume its data |
| mush.odyliao.cc/map | Site reachable in Chrome; displays GPS/precise-map lock with unlock/login controls | No authorized public precision feed or reuse terms verified. Visible default filter initially shows zero; this does not establish the total database size | Do not bypass access controls |
| LIUXVuse/pikmin-bloom-map | README describes Facebook-group scraping using logged-in cookies; records include scraped_at | scraped_at is scrape time, not current mushroom observation. No permission for redistributing contributors' records verified | Do not import as live sightings |
| pixlpirate/pikmin-map | README: GPLv3 app using OpenStreetMap for likely decor locations | App license does not make predicted decor points verified mushroom coordinates or active giants | Not a mushroom observation feed |
| Pickmin postcards atlas | Public pages show postcard mushroom spots and added dates | Added date is not active giant observation time; no verified feed/reuse permission | Candidate for contacting owner, not live ingestion |
| Consented maintainer-approved GitHub reports | Existing issue template and report_ingest.py | Explicit firsthand observation, timestamp, coordinate-publication consent, and radar-approved label required; observations expire after 90 minutes | Supported, but zero valid reports verified |

## Required evidence before enabling a feed

1. Owner-provided HTTPS endpoint and documented permission/license covering data redistribution.
2. Original source URL for each observation, timezone-aware observed_at, exact coordinates, explicit mushroom type and size.
3. Confirm timestamp means actual observation; ingestion/publication/scrape timestamps do not count.
4. Demonstrate stable updates and failure behavior. Never invent observations, use private game protocols, inject the game, or override location.

Feed secrets: FIXED_SOURCE_URL and MUSHROOM_SOURCE_URL.
Public permission references: repository variables FIXED_SOURCE_LICENSE_URL and MUSHROOM_SOURCE_LICENSE_URL.
The presence of a permission URL is an operational gate, not an automatic legal determination; a maintainer must verify its content before configuration.
GEMINI_API_KEY enables discovery links only; search results never become map observations automatically.

## Android connection checked

Official ADB found an authorized physical CPH2783 device. Pikmin Bloom is installed and a local screenshot was captured successfully.
Connection alone provides no global feed and does not authorize publishing the user's precise location.
No Root module, hook, GPS override, or third-party scanner was installed.

## Primary references

- https://github.com/odyliao-lab/pikmin-mush
- https://github.com/bittieshsu/pikmin-mush/blob/main/README.md
- https://mush.odyliao.cc/map
- https://github.com/LIUXVuse/pikmin-bloom-map/blob/main/README.md
- https://github.com/pixlpirate/pikmin-map
- https://pickmin-postcards.vercel.app/en
