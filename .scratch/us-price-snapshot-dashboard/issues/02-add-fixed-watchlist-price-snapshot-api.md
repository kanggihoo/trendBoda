Status: ready-for-agent

# Add Fixed Watchlist Price Snapshot API

## Parent

.scratch/us-price-snapshot-dashboard/PRD.md

## What to build

Expose a dashboard-oriented backend path that returns successful Price Snapshots for the fixed Owner Watchlist configured through environment settings. This slice should let the dashboard request the current fixed Watchlist without knowing Finnhub details, enforce the MVP 20-symbol limit, and skip invalid or unavailable symbols without hiding the rest of the Watchlist.

## Acceptance criteria

- [ ] Backend settings read the fixed Watchlist from `MARKET_WATCHLIST_SYMBOLS`.
- [ ] The default fixed Watchlist is `AAPL,NVDA,TSLA`.
- [ ] Watchlist symbols are trimmed, uppercased, and de-duplicated before provider calls.
- [ ] The Price Snapshot service rejects configured Watchlists above 20 symbols with a clear error.
- [ ] The backend exposes a dashboard-oriented Watchlist Price Snapshot endpoint.
- [ ] The endpoint returns successful Price Snapshot items for valid Watchlist symbols.
- [ ] Invalid or unavailable symbols are omitted from successful results and logged for diagnosis.
- [ ] If every symbol fails or the provider cannot be used, the endpoint returns an explicit API error instead of an empty success that hides a system failure.
- [ ] API response items include symbol, name, exchange, currency, current price, previous close, change, change percent, day open, day high, day low, provider, freshness, and last updated time where available.
- [ ] API tests cover successful Watchlist response, uppercase and de-duplication behavior, 20-symbol limit failure, invalid symbol skipping, and all-symbol failure behavior.

## Blocked by

- .scratch/us-price-snapshot-dashboard/issues/01-harden-finnhub-price-snapshot-provider.md
