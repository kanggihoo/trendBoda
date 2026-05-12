# Scheduled GeekNews Collection

TrendBoda should collect GeekNews Signals automatically after the first slice, without moving scheduler responsibility into FastAPI.

## Direction

- Run a separate scheduler process from FastAPI.
- Reuse shared backend factories for settings, database pool, repositories, provider adapters, fetch services, and Telegram sender setup.
- Support `run-once` for future cron, systemd timer, or external scheduler use.
- Support `run-forever` for a simple local or server worker that runs every two hours.
- Parse the full current GeekNews RSS feed on each run.
- Bulk insert new GeekNews Signals with database duplicate prevention.
- Use `ON CONFLICT DO NOTHING` so existing item snapshots are not rewritten.
- Return newly inserted items from the repository so Telegram push is based on actual inserts.
- Push every newly inserted GeekNews Signal to the Owner through existing Telegram configuration.
- Keep `/geeknews` as a manual/debug command for stored item lookup.

## Current Policy

- Fetch interval: every two hours.
- Push timing: immediately after a scheduled fetch when new GeekNews Signals were inserted.
- No new items: no Telegram message.
- Push size: no count limit in this slice; each new GeekNews Signal is sent as its own Telegram message.
- Dashboard: reads stored DB state through the backend API; it does not trigger scheduled fetches.

## Failure Policy

- RSS fetch or parse failure stops DB item insert and Telegram push for that run.
- DB insert failure stops Telegram push for that run.
- Telegram send failures are isolated per message; the scheduler continues attempting later new GeekNews Signals.
- Missing Telegram configuration skips push but does not block GeekNews collection.
- `run-forever` continues to the next tick after a failed run.
- `run-once` exits with failure for fetch, parse, or DB failures.
- Delivery tracking storage and automatic retry queues are deferred.

## Out of Scope

- Redis, arq, Celery, or APScheduler.
- Delivery tracking tables.
- Automatic retry queues for failed Telegram pushes.
- GeekNews AI summaries or preview notes.
- Original article body fetching.
- Multi-owner delivery routing.
- Cloud service definitions.

## Related Work

- `.scratch/scheduled-geeknews-telegram-push/PRD.md`
- `.scratch/geeknews-without-summary/PRD.md`
