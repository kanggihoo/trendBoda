Status: ready-for-agent

# Scheduled GeekNews Collection and Telegram Push PRD

## Problem Statement

The Owner can manually trigger GeekNews collection and can read stored GeekNews items through the dashboard or Telegram command flow, but TrendBoda does not yet decide when GeekNews should be collected or when new GeekNews Signals should be sent to the Owner. The current system has the API and storage pieces, but the Owner still has to remember to fetch and inspect items manually.

The Owner wants GeekNews to behave like a lightweight routine signal source: TrendBoda should periodically read the GeekNews RSS feed, store only newly seen items, and push those new GeekNews Signals to Telegram without requiring manual action. The dashboard should continue to read from the database, and `/geeknews` should remain available as a manual/debug command.

## Solution

Add a separate scheduler worker process for GeekNews collection and Telegram push. The scheduler should run independently from FastAPI, reuse the same application services through a shared bootstrap/factory layer, and execute a GeekNews scheduled job every two hours.

Each scheduled run should fetch the current GeekNews RSS feed, parse all items in the feed, bulk insert only new items into Postgres, and push every newly inserted GeekNews Signal to the Owner through the existing Telegram configuration and sender. Existing items should not be updated or re-pushed by default. The Next.js dashboard continues to read stored GeekNews items through the backend API.

The scheduled job should include a minimal explicit failure policy from day one. Fetch, parse, and database failures should stop push for that run. Telegram message failures should be isolated per GeekNews Signal so one failed Telegram send does not prevent later new Signals from being attempted. Delivery tracking storage and automatic retry queues remain out of scope.

## User Stories

1. As the Owner, I want TrendBoda to fetch GeekNews automatically every two hours, so that I do not need to trigger collection manually.
2. As the Owner, I want TrendBoda to parse the full current GeekNews RSS feed on every scheduled run, so that feed reordering or non-contiguous IDs do not cause missed items.
3. As the Owner, I want duplicate GeekNews items to be ignored by the database, so that repeated scheduled fetches do not create duplicate dashboard rows.
4. As the Owner, I want only newly inserted GeekNews Signals to be pushed to Telegram, so that I do not receive the same item repeatedly.
5. As the Owner, I want the scheduler to send a Telegram message when new GeekNews Signals appear, so that I see new developer trends without opening the dashboard.
6. As the Owner, I want no Telegram message when no new GeekNews Signals appear, so that routine checks do not create noise.
7. As the Owner, I want each new GeekNews Signal to be sent as its own Telegram message, so that Telegram's normal read and unread behavior can help me process items.
8. As the Owner, I want `/geeknews` to remain available, so that I can manually inspect recent stored GeekNews Signals for debugging or synchronization.
9. As the Owner, I want the Next.js dashboard to continue reading GeekNews items from the database, so that scheduled collection and dashboard display remain decoupled.
10. As the Owner, I want manual fetch API endpoints to remain available, so that local smoke tests and debugging can still trigger collection on demand.
11. As the Owner, I want Telegram bot token and allowed chat ID settings to be reused, so that this change does not introduce a second Telegram configuration path.
12. As the Owner, I want Telegram push failures to be logged without rolling back successful DB inserts, so that collection remains durable even if delivery fails.
13. As the Owner, I want the scheduler to run as a separate process from FastAPI, so that background work does not mix with HTTP request handling.
14. As the Owner, I want one local command or script to start the API and scheduler together during development, so that the separated process model does not make local use awkward.
15. As a future operator, I want the scheduler to support a one-shot mode, so that cron, systemd timers, or another external scheduler can run the same job later.
16. As a future operator, I want the scheduler to support a forever mode, so that a simple worker process can run the job every two hours without Redis or a task queue.
17. As a future agent, I want FastAPI and the scheduler to share service construction code, so that DB pool, repositories, provider adapters, and Telegram sender setup do not drift.
18. As a future agent, I want the GeekNews repository to return newly inserted items, so that Telegram push can be based on actual DB insert results rather than guessed feed order.
19. As a future agent, I want the bulk insert behavior to be testable in isolation, so that duplicate prevention and inserted item selection remain reliable.
20. As a future agent, I want this slice to avoid Redis, arq, Celery, and delivery tracking storage, so that the first scheduled implementation stays small.
21. As the Owner, I want RSS fetch or parse failures to stop that scheduled run before database writes or Telegram push, so that broken feed data does not create confusing output.
22. As the Owner, I want database write failures to stop Telegram push, so that TrendBoda does not send Signals that were not durably stored.
23. As the Owner, I want one Telegram message failure to leave the remaining new Signals eligible for send attempts in the same run, so that a single bad message or transient Telegram error does not block the whole batch.
24. As the Owner, I want scheduler failures to be visible in logs, so that I can diagnose missed collection or delivery without a delivery tracking table.

## Implementation Decisions

- Run GeekNews scheduling outside FastAPI as a separate backend process.
- Add a scheduler entrypoint with at least two modes: `run-once` and `run-forever`.
- Default scheduled interval is two hours.
- Make the interval configurable through environment or settings, with `7200` seconds as the default.
- Keep FastAPI route handlers as manual trigger and read APIs; the scheduler should not call the HTTP API to perform internal work.
- FastAPI and scheduler should both call shared application services directly.
- Add or clarify a shared bootstrap/factory layer that creates settings, DB pool, repositories, GeekNews provider, GeekNews fetch service, Telegram sender, and scheduled job services.
- The scheduled job should call GeekNews fetch behavior directly, then push newly inserted items through the existing Telegram sender.
- Reuse existing Telegram bot token and allowed chat ID settings.
- Require at least one allowed Telegram chat ID for automatic push; if none is configured, the scheduler should collect data and log that push was skipped.
- Parse all items returned by the GeekNews RSS feed on each fetch.
- Replace per-item insert roundtrips with a bulk insert repository operation where practical.
- Use the existing unique identity for GeekNews items to prevent duplicates.
- Prefer `ON CONFLICT DO NOTHING` for duplicate GeekNews items.
- Preserve first-seen item snapshots; existing rows should not have title, content, fetched time, or updated time changed by routine fetches.
- The repository should return newly inserted stored GeekNews items or a result object containing both inserted count and inserted items.
- Telegram push should use the inserted items returned by the repository, not a separate query based only on timestamps.
- Telegram push should send every newly inserted GeekNews Signal as its own Telegram message.
- Do not truncate scheduled Telegram push by count in this slice.
- Telegram read and unread state is handled by the Telegram client, not by TrendBoda storage.
- Telegram push failure should not roll back GeekNews DB inserts.
- Telegram send failures should be isolated per message: continue attempting later new GeekNews Signals in the same run after an individual send failure.
- RSS fetch failures should record a failed fetch run when possible, skip DB item insert, skip Telegram push, and log the failure.
- RSS parse failures should record a failed fetch run when possible, skip DB item insert, skip Telegram push, and log the failure.
- Database insert failures should skip Telegram push and log the failure.
- Missing Telegram token or allowed chat ID should not block GeekNews collection; the scheduler should store new items and log that push was skipped.
- The scheduler should not wrap DB insert and Telegram push in one transaction because Telegram delivery is an external side effect that cannot be rolled back.
- `run-forever` should survive a failed scheduled run and continue to the next tick.
- `run-once` should return a failing process status for fetch, parse, or DB failures; Telegram send failures should be logged with a summarized failure count.
- Scheduler runs should log fetch count, inserted count, attempted push count, successful push count, failed push count, skipped push reason, and errors.
- Keep `/geeknews` as a manual/debug command that reads recent stored GeekNews Signals.
- Keep `POST /geeknews/fetch-runs` as a manual fetch trigger for local debugging and smoke checks.
- Do not add delivery tracking storage in this slice.
- Do not add Redis, arq, Celery, APScheduler, or another task queue in this slice.
- Design the scheduled job around a simple `run_once` application service so that a future arq worker, cron command, or systemd timer can call the same behavior.

## Testing Decisions

- Tests should verify external behavior and stable service contracts, not private implementation details.
- Repository tests should cover bulk insert, duplicate prevention, unchanged existing rows, and returning newly inserted items.
- GeekNews scheduled job tests should cover no new items, every new item pushed as an individual message, missing chat ID skip behavior, fetch failure behavior, parse failure behavior, DB failure behavior, and per-message Telegram failure isolation.
- Telegram message formatting tests should cover scheduled push output separately from `/geeknews` command output.
- Scheduler entrypoint tests should cover argument parsing or mode selection where practical without sleeping for two hours.
- FastAPI route tests should remain focused on manual fetch and read API behavior.
- Existing Telegram command tests should continue to prove `/geeknews` reads stored items and does not depend on scheduled push.
- No default test should require live GeekNews RSS, live Telegram, Redis, Docker, or OpenRouter.
- Integration tests may cover repository bulk insert behavior against Postgres if the repo already has integration test support.
- Smoke documentation should explain how to run the scheduler in one-shot mode and forever mode.

## Out of Scope

- Redis, arq, Celery, APScheduler, or task queue adoption.
- Delivery tracking tables.
- Automatic retry queues for failed Telegram pushes.
- Scheduled push count limits or batching policies.
- Multi-owner delivery routing.
- Telegram delivery history dashboard.
- Automatic AI summary or AI preview note generation for GeekNews.
- Fetching original linked article bodies.
- Changing the Next.js dashboard into a live push client.
- Replacing the existing manual GeekNews fetch API.
- Removing `/geeknews`.
- Cloud deployment, systemd unit files, Docker Compose service definitions, or EC2 operations automation.
- Market Sources, Disclosure Sources, Market Questions, Investment Analysis, and Price Snapshots.

## Further Notes

- This PRD follows the `CONTEXT.md` decision that GeekNews uses **GeekNews Signals** for scanning and source-link navigation.
- The scheduler is an automatic trigger, not a replacement for the backend API.
- The backend API remains useful for manual fetch, local smoke tests, dashboard reads, and Telegram command reads.
- The first implementation should stay intentionally simple: separate process, shared bootstrap, direct service calls, bulk insert, and Telegram push.
- If scheduled jobs grow beyond one or two simple routines, the same `run_once` job service can later be moved behind arq or another task queue without rewriting the GeekNews domain flow.
