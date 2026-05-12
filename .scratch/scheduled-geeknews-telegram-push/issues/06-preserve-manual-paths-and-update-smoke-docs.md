Status: ready-for-agent
Type: AFK

# Preserve Manual Paths And Update Smoke Docs

## Parent

.scratch/scheduled-geeknews-telegram-push/PRD.md

## What to build

Close the scheduled GeekNews slice by proving existing manual owner paths still work and documenting how to run the new scheduler. `/geeknews`, manual fetch APIs, and the Next.js dashboard should continue reading stored GeekNews Signals from the backend, while smoke documentation should explain one-shot and forever scheduler modes.

## Acceptance criteria

- [ ] Telegram `/geeknews` remains a manual/debug command that reads recent stored GeekNews Signals.
- [ ] Manual GeekNews fetch endpoints remain available for local debugging and smoke checks.
- [ ] The Next.js dashboard continues to read stored GeekNews items through the backend API.
- [ ] Dashboard behavior does not depend on scheduler push state or Telegram delivery state.
- [ ] Smoke or local setup docs explain how to run scheduler `run-once`.
- [ ] Smoke or local setup docs explain how to run scheduler `run-forever`.
- [ ] Docs describe the two-hour default interval and how to override it.
- [ ] Docs state that delivery tracking storage and automatic retry queues are out of scope.
- [ ] Tests or checks prove existing manual fetch, item listing, and `/geeknews` behavior remain compatible.

## Blocked by

- .scratch/scheduled-geeknews-telegram-push/issues/05-add-scheduler-entrypoint-modes.md
