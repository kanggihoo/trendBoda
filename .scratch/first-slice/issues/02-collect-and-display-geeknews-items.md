Status: ready-for-agent
Type: AFK

# Collect and display GeekNews items

## Parent

.scratch/first-slice/PRD.md

## What to build

Implement the first real Source path for TrendBoda by fetching GeekNews RSS, parsing it into normalized Developer Trend Source items, storing items with duplicate prevention, exposing item and fetch APIs, and showing recent items in the dashboard. The completed slice should be demoable by running a manual fetch and seeing GeekNews items appear in the web dashboard.

## User stories covered

- 1. Fetch GeekNews RSS
- 2. Parse GeekNews RSS into normalized records
- 3. Store GeekNews items in Postgres
- 4. Prevent duplicate GeekNews items
- 5. Record GeekNews fetches
- 6. See recent GeekNews items in the dashboard
- 7. Open original GeekNews items from the dashboard
- 8. See publish time and fetch time
- 9. Trigger a manual GeekNews fetch
- 26. Expose GeekNews item APIs
- 29. Show GeekNews items in the Next.js dashboard
- 39. Test parser, storage, API, and dashboard behavior

## Acceptance criteria

- [x] GeekNews RSS is fetched from `https://feeds.feedburner.com/geeknews-feed` through a provider adapter.
- [x] RSS XML is normalized into stable application-level item data.
- [x] GeekNews items are stored in Postgres with duplicate prevention.
- [x] Fetch runs are recorded with enough data to inspect freshness and failures later.
- [x] FastAPI exposes endpoints to manually fetch GeekNews and list stored items.
- [x] The dashboard shows recent GeekNews items with title, source link, publish time, and fetch time.
- [x] Re-running the fetch does not create duplicate dashboard rows for the same item.
- [x] Parser tests cover valid RSS, missing optional fields, HTML entities, duplicate identifiers, item ordering, and malformed XML behavior.
- [x] Repository tests cover insertion, duplicate prevention, and fetch run recording.
- [x] API and dashboard tests cover successful, empty, and error states.

## Blocked by

- .scratch/first-slice/issues/01-bootstrap-local-trendboda-skeleton.md
