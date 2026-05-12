Status: ready-for-agent

# Polish Price Snapshot Quota-Friendly Flow

## Parent

.scratch/us-price-snapshot-dashboard/PRD.md

## What to build

Connect and harden the end-to-end Price Snapshot dashboard flow so it remains quota-friendly and diagnosable. This slice should verify that dashboard-demand fetching respects cache TTLs, provider failures degrade to stale data when possible, skipped symbols are visible in logs, and local documentation explains the fixed Watchlist and Finnhub API key setup.

## Acceptance criteria

- [ ] End-to-end checks prove dashboard refreshes within the quote TTL do not create unnecessary Finnhub quote calls.
- [ ] End-to-end checks prove stale fallback is surfaced in the API and dashboard when Finnhub is temporarily unavailable and stale data exists.
- [ ] Provider failures and skipped symbols are logged with enough context for local diagnosis without exposing secrets.
- [ ] `FINNHUB_API_KEY` and `MARKET_WATCHLIST_SYMBOLS` are documented for local setup.
- [ ] Documentation states that `MARKET_WATCHLIST_SYMBOLS` defaults to `AAPL,NVDA,TSLA`.
- [ ] Documentation states that the fixed Watchlist is capped at 20 symbols.
- [ ] Documentation states that editable Watchlist CRUD, DB persistence, charts, Telegram commands, scheduled price pushes, metrics, earnings, websocket streaming, Korean market coverage, and paid providers are out of scope for this MVP.
- [ ] The live Finnhub integration test remains opt-in and is not part of the default test suite.
- [ ] Default backend and web checks pass without live Finnhub, Redis, Docker, Telegram, OpenRouter, or a paid provider account.

## Blocked by

- .scratch/us-price-snapshot-dashboard/issues/03-add-price-snapshot-cache-and-stale-fallback.md
- .scratch/us-price-snapshot-dashboard/issues/04-render-dashboard-price-snapshot-table.md
