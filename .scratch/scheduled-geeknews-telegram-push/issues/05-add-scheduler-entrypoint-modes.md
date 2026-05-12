Status: done
Type: AFK

# Add Scheduler Entrypoint Modes

## Parent

.scratch/scheduled-geeknews-telegram-push/PRD.md

## What to build

Add a scheduler worker entrypoint that can run the scheduled GeekNews job once or forever. The one-shot mode should support future cron or systemd timer use. The forever mode should run every two hours by default, survive failed scheduled runs, and continue to the next tick.

## Acceptance criteria

- [ ] A scheduler entrypoint supports a `run-once` mode.
- [ ] A scheduler entrypoint supports a `run-forever` mode.
- [ ] The default scheduler interval is two hours.
- [ ] The scheduler interval is configurable through settings or environment with `7200` seconds as the default.
- [ ] `run-once` returns a failing process status for fetch, parse, or database failures.
- [ ] `run-once` logs Telegram send failures with a summarized failure count.
- [ ] `run-forever` continues to the next tick after failed scheduled runs.
- [ ] Entry point behavior is testable without sleeping for two hours.
- [ ] No Redis, arq, Celery, APScheduler, or external task queue is introduced.
- [ ] Local run instructions document both scheduler modes.

## Blocked by

- .scratch/scheduled-geeknews-telegram-push/issues/03-run-scheduled-geeknews-fetch-once.md
- .scratch/scheduled-geeknews-telegram-push/issues/04-push-every-new-geeknews-signal-to-telegram.md
