# US Price Snapshot

TrendBoda should add a dashboard-first Price Snapshot slice for US stocks and ETFs before adding editable Watchlist management, Telegram price commands, scheduled price briefings, or Korean market coverage.

## Direction

- Use Finnhub as the first US Market Source provider for Price Snapshots.
- Limit the MVP to US-listed stocks and ETFs.
- Represent broad US indexes through tradable ETF proxies instead of direct index symbols in the MVP.
- Keep the first Watchlist as a fixed owner-configured list from environment settings.
- Allow up to 20 Watchlist symbols in the MVP.
- Design the fixed Watchlist so it can later be replaced by owner-editable add/remove behavior without changing the Price Snapshot contract.
- When owner-editable Watchlist management is added later, enforce the same 20-symbol limit at the add/update boundary before symbols can enter the Watchlist.
- Show Price Snapshots in the Next.js dashboard first.
- Fetch Price Snapshots on dashboard demand rather than through a scheduler in the MVP.
- Do not add Telegram price commands or scheduled price pushes in the MVP.
- Do not store Price Snapshots in Postgres in the MVP.
- Do not use AI for Price Snapshots.

## Finnhub API Scope

- Use `/quote` for current or recent quote data.
- Use `/stock/profile2` for symbol metadata such as company name, exchange, currency, industry, and market capitalization when available.
- Use `/stock/market-holiday?exchange=US` as market-calendar support.
- Do not use metrics, earnings, company news, or websocket streaming in the MVP.

## Initial Watchlist

- Start local verification with `AAPL`, `NVDA`, and `TSLA`.
- Use ETF proxies when the Owner wants broad index exposure in the dashboard:
  - Nasdaq 100: `QQQ` instead of `^NDX`
  - S&P 500: `SPY` instead of `^GSPC`
  - Dow Jones Industrial Average: `DIA` instead of `^DJI`
- Do not treat direct index symbols as in-scope until a separate Market Index Snapshot policy exists.

## API Policy

- Expose a dashboard-oriented backend endpoint that accepts up to 20 symbols.
- For the fixed-env MVP, reject requests or configured Watchlists above 20 symbols at the Price Snapshot service/API boundary.
- Normalize symbols to uppercase and de-duplicate them before provider calls.
- Return successful Price Snapshot items; invalid or unavailable symbols should not break the full response.
- Treat Finnhub invalid-symbol quote responses with zero price and zero timestamp as unavailable.
- Log unavailable symbols and provider failures for diagnosis.
- Use owner-only display assumptions because Finnhub free usage is personal-use oriented.

## Cache Policy

- Cache quote data in memory for 60 seconds.
- Keep quote stale fallback data for up to five minutes when Finnhub is temporarily unavailable or rate-limited.
- Cache profile data in memory for 24 hours.
- Cache US market holiday data in memory for 24 hours or until the next local market-calendar refresh boundary.
- Define caching behind a small Price Snapshot cache interface so the MVP in-process cache can later be replaced by Redis without changing provider, service, API, or dashboard contracts.
- On each dashboard request, decide per symbol whether to return fresh cached data, call Finnhub for missing or expired data, or return stale cached data when Finnhub is temporarily unavailable.
- Keep an internal provider rate guard below Finnhub's free-tier 60 API calls per minute.
- Prefer cache hits over provider calls for repeated dashboard refreshes.

## Dashboard Policy

- Dashboard is the first consumer.
- Display dense, scannable table-like rows for Watchlist symbols on desktop.
- Use compact stacked rows on mobile while preserving the same scan order.
- Include symbol, name, exchange, currency, current price, previous close, change, change percent, day open, day high, day low, provider, and last updated time where available.
- Show freshness when a quote comes from stale fallback data.
- Do not auto-refresh in the MVP; use manual refresh and respect cache TTL.
- Do not introduce a broad reusable DataTable abstraction in the MVP unless repeated table behavior already exists.

## Out of Scope

- Editable Watchlist CRUD.
- Korean stocks or Korean ETFs.
- Direct market index snapshots.
- Price Snapshot persistence.
- Price alerts, thresholds, or Urgent Alerts.
- Routine Briefing integration.
- Telegram `/price` or `/prices` commands.
- Finnhub websocket streaming.
- Fundamental metrics, earnings, and company news.
- Paid provider integration.
