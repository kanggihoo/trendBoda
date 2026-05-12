Status: done
Type: AFK

# Share Backend Bootstrap Between API And Scheduler

## Parent

.scratch/scheduled-geeknews-telegram-push/PRD.md

## What to build

Create or clarify shared backend bootstrap behavior so FastAPI and the future scheduler worker construct common dependencies the same way. Both entrypoints should use the same settings, database pool, repositories, GeekNews provider, GeekNews fetch service, and Telegram sender setup instead of duplicating wiring.

## Acceptance criteria

- [ ] FastAPI still starts and exposes existing health and GeekNews endpoints.
- [ ] Shared bootstrap creates settings, database pool, repositories, GeekNews provider, and GeekNews fetch service for FastAPI use.
- [ ] Shared bootstrap exposes construction behavior that a scheduler entrypoint can reuse without importing FastAPI route modules.
- [ ] Telegram sender setup reuses the existing Telegram bot token and allowed chat ID settings.
- [ ] FastAPI route handlers remain thin and call application services directly.
- [ ] No scheduler loop is embedded inside FastAPI startup or background tasks.
- [ ] Tests cover FastAPI dependency wiring or app startup behavior after the bootstrap change.
- [ ] Backend docs or existing setup notes remain consistent with the shared bootstrap direction.

## Blocked by

- .scratch/scheduled-geeknews-telegram-push/issues/01-bulk-insert-new-geeknews-signals.md
