Status: ready-for-agent
Type: AFK

# Harden GeekNews slice and API boundaries

## Parent

.scratch/first-slice/PRD.md

## What to build

Tighten the completed GeekNews first-slice implementation without expanding scope beyond the existing GeekNews path. Separate FastAPI API wiring from route handlers and response schemas, then close the small acceptance gaps found after issue 02: failed fetch runs should be recorded when possible, the dashboard should show both publish time and fetch time, and tests should cover the parser/API/dashboard behavior already promised by the first-slice PRD.

This issue is a follow-up to issue 02. It should not rename database tables, API paths, or the provider-specific GeekNews implementation into generic Developer Trend Source modules yet.

## User stories covered

- 5. Record GeekNews fetches
- 8. See publish time and fetch time
- 26. Expose GeekNews item APIs
- 29. Show GeekNews items in the Next.js dashboard
- 39. Test parser, storage, API, and dashboard behavior

## Acceptance criteria

- [ ] `backend/src/trendboda/app.py` owns FastAPI app creation, lifespan setup, and router registration only.
- [ ] FastAPI dependency helpers live outside `app.py` and read repositories from `request.app.state`.
- [ ] GeekNews routes/controllers live outside `app.py`.
- [ ] GeekNews Pydantic API response models live outside `app.py`.
- [ ] Existing `/health`, `/geeknews/items`, and `/geeknews/fetch` API behavior remains compatible.
- [ ] Failed GeekNews fetch attempts record a `geeknews_fetch_runs` row with `status = 'failure'`, `item_count = 0`, and an inspectable error message when possible.
- [ ] The dashboard shows both publish time and fetch time for recent GeekNews items.
- [ ] Parser tests cover valid RSS, missing optional fields, HTML entities, duplicate identifiers, item ordering, and malformed XML behavior.
- [ ] API tests cover successful item listing, empty item listing, successful fetch, and fetch failure recording behavior.
- [ ] Dashboard tests or checks cover loading, empty, ready, and error states for GeekNews items.
- [ ] No broad source-domain refactor is performed; GeekNews remains the provider-specific first-slice path.

## Blocked by

- .scratch/first-slice/issues/02-collect-and-display-geeknews-items.md
