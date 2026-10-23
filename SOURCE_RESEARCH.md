# Source verification — 2026-10-23 (Asia/Taipei)

**Production acceptance: FAIL. No permitted current giant-mushroom feed has been verified.**
This records evidence and uncertainty; public visibility does not establish redistribution permission.

| Candidate | Evidence | Permission / freshness | Decision |
| --- | --- | --- | --- |
| odyliao-lab/pikmin-mush | GitHub repository API and contents both return 404 on this check | No available license or feed contract to verify at this address | Not configured |
| bittieshsu/pikmin-mush | Public README points to the above name and mush.odyliao.cc; repository metadata has license=null; pushed_at 2026-10-06T16:01:23Z | README describes Root Android Zygisk hooks, injected game data extraction and location override. Code update time is not an observation time. No permission for this radar to republish data was verified | Do not deploy its scanner or consume its data |
| mush.odyliao.cc/map and /api/mushrooms | Website and documented public API reachable. At 2026-10-23 15:15:06 +08, API count=24,722, returned=500; all 500 have null latitude/longitude, gps_access.authorized=false. Latest last_observed_at=15:15:05 +08 | API has recent timestamps but exact coordinates are access-controlled; reuse permission remains unverified. Website default filter showing zero is not total database size | Do not bypass GPS access controls or import records as mappable observations |
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
The visible player is level 7; official support says mushroom battles unlock at level 8. This account cannot currently supply an in-game mushroom detail for validation.
Official reference: https://niantic.helpshift.com/hc/en/23-pikmin-bloom/faq/3039-mushrooms-1676271507/

## Primary references

- https://github.com/odyliao-lab/pikmin-mush
- https://github.com/bittieshsu/pikmin-mush/blob/main/README.md
- https://mush.odyliao.cc/map
- https://github.com/LIUXVuse/pikmin-bloom-map/blob/main/README.md
- https://github.com/pixlpirate/pikmin-map
- https://pickmin-postcards.vercel.app/en

## Additional source tests — 2026-10-23 17:41–17:46 +08

No authorization-request email was sent. The user explicitly instructed not to send email and to continue testing.

### Treelazy live mushroom map
- Public map https://treelazy.com/pikmushroom-en loaded successfully in Chrome.
- Displayed total: 1,196 (1,190 current round plus six previous round).
- Displayed content update: 2026-10-23 16:44:59 in the browser's displayed timezone. First three visible rows showed found times 16:43/16:42. These human-readable times alone are not yet a verified timezone-aware observed_at contract.
- The normal Show coordinates control successfully revealed a coordinate for one small blue mushroom; no login or access-control bypass was used.
- Selecting Giant returned 0 rows, not 1,196 giant sightings.
- Other rows labelled green were several hours old; a green badge is not sufficient for the radar's 90-minute freshness requirement.
- Terms https://treelazy.com/dist/disclaimer welcome attributed reference and prohibit disruptive bulk automation. They do not establish an explicit recurring API/whole-dataset redistribution contract or the provenance of the mushroom collection. The source remains disabled pending a sufficient permission/data contract.

### PikminPosts
- Terms https://www.pikminposts.com/info/terms.php were read directly in Chrome (updated 2026-05-30).
- Contributor content rights are granted to that Site; this was not verified as a grant to this radar or a public data license.
- Terms restrict technical abuse and automated activity that disrupts the service.
- Postcard/map availability does not establish the present size or observation time of a live giant.
- No automatic collection or republication was enabled.

### svmax3065/pikmin-mushroom-watch
- Public app https://pikmin-mushroom-watch.vercel.app connected and displayed one matching giant-labelled record.
- A single public record read using the same public data path documented by the app showed createdAt and updatedAt = 2026-09-28T02:52:25.692Z.
- That record had no usable exact coordinates or observed_at. It cannot satisfy current observation acceptance.
- Source code sets the displayed update time to the browser's current time on receipt, not the game observation time.
- Classification is a description keyword match, not independent proof of mushroom size.
- Repository license metadata is null. No data reuse permission was verified.
- No raw record, contributor identifiers, or extra personal metadata is republished here.

### Other public projects reviewed
- flyskyg/MushroomTracker: MIT software, but a manually configured respawn timer; no continuing mushroom observation feed established.
- Weihsuan-0723/pikmin-mushroom-map: README explicitly describes manual entry, optional externally supplied feed, and random demonstration rows. No actual live feed is configured by this project.
- frobel0520/pikmin-mushroom-room: README describes a private family timer board and no redistribution license; not a public observation feed.
- yachaejjim/pikmin-mushrooms-storage: personal storage/authentication-based app; no permitted current public feed established.
- wei5549/pikmin-global-mushroom: frontend points to an external Worker; no data license or independently verified provenance contract found. No records imported.

### Collector contract execution
Seven read-only checks against the current radar.py passed:
1. Masked coordinates do not create giant observations.
2. Missing observed_at does not create giant observations.
3. updated_at alone cannot replace observed_at.
4. Six-hour-old observations are rejected.
5. Future observations are rejected.
6. A small mushroom cannot become a giant.
7. The earlier privately checked phone observation is now older than 90 minutes and is excluded.

These checks exercised private/contract input locally. Nothing was published to mushrooms.json and no timestamp was refreshed to make an old sighting appear current.

### Phone and giant availability
- The user has now demonstrated real mushroom detail plus a coordinate destination from normal gameplay. The earlier level-7 blocker is obsolete.
- The user confirmed at this follow-up that currently visible mushrooms are only normal and small. No giant has been verified on the phone.
- Official event schedule https://pikminbloom.com/news/oct26-halloweenevent lists Giant Halloween Mushrooms on October 24–25 and October 28–31 (local time), following the earlier October weekends.
- Event dates are candidate timing information, never evidence of a particular live giant.

**Current outcome: source-contract tests PASS; automatic permitted source and real giant end-to-end acceptance remain FAIL.**
