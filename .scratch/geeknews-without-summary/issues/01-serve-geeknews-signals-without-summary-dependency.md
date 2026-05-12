Status: done
Type: AFK

# Serve GeekNews Signals Without Summary Dependency

## Parent

.scratch/geeknews-without-summary/PRD.md

## What to build

Make the backend GeekNews owner flow serve stored GeekNews Signals without requiring AI summary data. The Owner should be able to fetch and list GeekNews Signals with title, short description, publish time, fetch time, and links, while existing RSS collection, duplicate prevention, fetch run recording, and non-summary item retrieval remain unchanged.

If summary fields remain in an API response for compatibility, they must be optional and not treated as required for a complete GeekNews Signal.

## User stories covered

- 1. Show GeekNews items without automatic AI summary
- 5. Keep GeekNews RSS fetching and duplicate prevention unchanged
- 6. Keep stored GeekNews item retrieval unchanged for non-summary fields
- 8. Avoid requiring summary data in GeekNews API behavior
- 12. Avoid broad database churn
- 14. Prove GeekNews still fetches and displays items without summaries

## Acceptance criteria

- [x] GeekNews fetch and list APIs work when stored items have no summary data.
- [x] GeekNews API responses expose title, short description, publish time, fetch time, and links as the default item data.
- [x] Missing summary data is not treated as an incomplete or error state for GeekNews Signals.
- [x] GeekNews RSS fetching, duplicate prevention, fetch run recording, and item retrieval keep existing behavior for non-summary fields.
- [x] Backend tests cover list and fetch behavior for GeekNews items without summaries.
- [x] No live OpenRouter, live Telegram, or live GeekNews network access is required by default tests.

## Blocked by

None - can start immediately
