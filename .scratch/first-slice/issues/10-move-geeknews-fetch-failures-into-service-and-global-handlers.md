Status: ready-for-agent
Type: AFK

# Move GeekNews fetch failures into service and global handlers

## Parent

.scratch/first-slice/PRD.md

## What to build

Refactor backend error handling around the current GeekNews first-slice API without changing the public success response shape or introducing a new API error envelope. Move GeekNews fetch orchestration into a service layer, keep fetch-run recording close to the GeekNews workflow, and register global FastAPI exception handlers for app-level and unexpected exceptions.

This issue should remove provider-level `try`/`except` handling from route handlers. Route handlers should call services, services should own workflow-specific side effects such as failure fetch-run recording, and global handlers should translate app exceptions into HTTP responses and logs.

## User stories covered

- 5. Record GeekNews fetches
- 9. Trigger a GeekNews fetch manually during local development
- 25. Expose health checks
- 26. Expose GeekNews item APIs
- 39. Test parser, storage, API, and dashboard behavior

## Acceptance criteria

- [x] GeekNews fetch orchestration lives in `GeekNewsFetchService`, not the route handler.
- [x] GeekNews fetch endpoint has no provider-level `try`/`except`.
- [x] Failed GeekNews provider fetch records a failure fetch run in the service layer.
- [x] The service raises an app-level exception for GeekNews fetch failure.
- [x] FastAPI app registers global exception handlers outside route modules.
- [x] The global handler maps GeekNews fetch failure to the existing `502 {"detail": "GeekNews fetch failed"}` response.
- [x] The global handler logs expected app exceptions with request method, request path, and exception code.
- [x] The global handler logs unexpected exceptions with stack trace and returns `500 {"detail": "Internal server error"}`.
- [x] Existing `/health`, `/geeknews/items`, and `/geeknews/fetch` API behavior remains compatible.
- [x] Tests cover service success, service failure recording, API failure mapping, and unexpected exception handling.
- [x] No API error envelope contract is introduced in this issue.
- [x] No broad source-domain refactor is performed; GeekNews remains the provider-specific first-slice path.

## Blocked by

- .scratch/first-slice/issues/07-harden-geeknews-slice-and-api-boundaries.md

## Comments

- 2026-05-09: Implemented GeekNews fetch service, app-level exceptions, and global exception handlers. Issue 11 subsequently replaced the temporary `{"detail": ...}` error body with the standardized error contract.
