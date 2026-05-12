Status: ready-for-agent
Type: AFK

# Run Scheduled GeekNews Fetch Once

## Parent

.scratch/scheduled-geeknews-telegram-push/PRD.md

## What to build

Add a scheduled GeekNews job service with a one-run operation that performs the collection portion of the scheduled flow. The job should call the shared GeekNews fetch behavior directly, collect newly inserted GeekNews Signals, and stop before Telegram push when fetch, parse, or database persistence fails.

## Acceptance criteria

- [ ] A scheduled GeekNews job exposes a `run_once`-style operation that can be called without FastAPI.
- [ ] The job fetches GeekNews RSS through the existing provider path.
- [ ] The job stores new GeekNews Signals through the bulk insert repository behavior.
- [ ] When no new GeekNews Signals are inserted, the job completes without Telegram push work.
- [ ] RSS fetch failures record a failed fetch run when possible, skip DB item insert, skip Telegram push, and are logged.
- [ ] RSS parse failures record a failed fetch run when possible, skip DB item insert, skip Telegram push, and are logged.
- [ ] Database insert failures skip Telegram push and are logged.
- [ ] Missing Telegram token or allowed chat ID does not fail collection; the job logs that push is skipped.
- [ ] The job reports fetch count, inserted count, skipped push reason, and errors in a testable result or logs.
- [ ] Unit tests cover no new items, missing Telegram configuration, fetch failure, parse failure, and database failure behavior.

## Blocked by

- .scratch/scheduled-geeknews-telegram-push/issues/01-bulk-insert-new-geeknews-signals.md
- .scratch/scheduled-geeknews-telegram-push/issues/02-share-backend-bootstrap-between-api-and-scheduler.md
