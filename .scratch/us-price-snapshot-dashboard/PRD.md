Status: ready-for-agent

# US Price Snapshot Dashboard PRD

## Problem Statement

The Owner can inspect GeekNews Signals and AI cost data in TrendBoda, but the system still has no way to show deterministic market prices for the Owner's watched US stocks and ETFs. The current product can discuss market-related concepts in its domain language, but it does not yet provide a Price Snapshot that helps the Owner quickly see whether watched US market names are up, down, stale, or unavailable.

The Owner wants the next market-data slice to stay small and free to operate. TrendBoda should first prove that it can fetch current or recent US stock and ETF quotes from Finnhub, protect the free-tier quota with caching, and show a compact dashboard view for a fixed Watchlist before adding editable Watchlist management, Telegram price commands, scheduled price collection, historical charts, or AI-backed analysis.

## Solution

Add a dashboard-first US Price Snapshot MVP. TrendBoda will use Finnhub as the first US Market Source provider, read a fixed Watchlist from environment settings, fetch Price Snapshot data on dashboard demand, cache provider responses in process, and render successful Watchlist items as dense table-like rows in the Next.js dashboard.

The MVP will support US-listed stocks and ETFs only. It will not store Price Snapshots in Postgres, run a scheduler, push price data to Telegram, draw charts, use AI, or fetch fundamental metrics and earnings. Broad US index exposure should be represented through ETF proxies such as QQQ, SPY, and DIA rather than direct index symbols.

## User Stories

1. As the Owner, I want to open the dashboard and see Price Snapshots for my fixed Watchlist, so that I can quickly scan watched US stocks and ETFs.
2. As the Owner, I want the initial Watchlist to include AAPL, NVDA, and TSLA, so that local verification starts with stable US stock symbols.
3. As the Owner, I want the Watchlist to be configurable through environment settings, so that I can change the first fixed list without database work.
4. As the Owner, I want the MVP Watchlist capped at 20 symbols, so that Finnhub free-tier usage stays predictable.
5. As the Owner, I want Price Snapshots to include current or recent price, previous close, change, change percent, open, high, low, and last updated time, so that I can understand the basic market move without AI explanation.
6. As the Owner, I want company or ETF metadata such as name, exchange, and currency when available, so that ticker symbols are easier to read.
7. As the Owner, I want unavailable or invalid symbols to be skipped rather than breaking the whole dashboard, so that one bad Watchlist entry does not hide every other price.
8. As the Owner, I want stale prices to be labeled when Finnhub is temporarily unavailable, so that I know the data is a recent fallback rather than a fresh provider response.
9. As the Owner, I want repeated dashboard refreshes to use cached data when possible, so that I do not waste Finnhub free-tier calls.
10. As the Owner, I want manual refresh rather than auto-refresh in the MVP, so that the dashboard stays quiet and quota-friendly.
11. As the Owner, I want a table-like dashboard layout on desktop, so that I can compare watched symbols quickly.
12. As the Owner, I want compact stacked rows on mobile, so that the same Price Snapshot data remains readable on smaller screens.
13. As the Owner, I want market movement colors for up, down, and neutral moves, so that I can scan direction quickly.
14. As the Owner, I want broad index exposure to use ETF proxies such as QQQ, SPY, and DIA, so that the MVP avoids direct index-symbol ambiguity.
15. As the Owner, I want Price Snapshots to avoid OpenRouter and AI, so that deterministic prices do not create AI cost or unsupported investment explanations.
16. As a future agent, I want Finnhub access isolated behind a provider adapter, so that future provider replacement or fallback does not rewrite dashboard code.
17. As a future agent, I want caching isolated behind a small Price Snapshot cache interface, so that the in-process cache can later be replaced by Redis without changing provider, service, API, or dashboard contracts.
18. As a future agent, I want the Price Snapshot service to choose fresh cache, provider fetch, or stale fallback per symbol, so that cache behavior is testable in isolation.
19. As a future agent, I want the backend API to expose a dashboard-oriented Watchlist endpoint, so that the dashboard does not need to know provider-specific Finnhub details.
20. As a future agent, I want the fixed Watchlist shape to be compatible with later editable Watchlist add/remove behavior, so that the MVP does not block future Watchlist CRUD.
21. As a future agent, I want the later editable Watchlist flow to enforce the same 20-symbol limit at the add/update boundary, so that symbols cannot enter the Watchlist beyond the free-tier policy.
22. As a future agent, I want live Finnhub tests to remain opt-in integration tests, so that default tests do not depend on live network calls or a real API key.
23. As a future operator, I want provider failures and skipped symbols logged, so that Finnhub or Watchlist problems can be diagnosed without showing raw provider errors to the Owner.

## Implementation Decisions

- Build a US Price Snapshot slice for dashboard use before adding Telegram, scheduled price collection, editable Watchlist management, historical charts, or Korean market support.
- Use Finnhub as the first US Market Source provider.
- Use Finnhub `/quote` for current or recent quote data.
- Use Finnhub `/stock/profile2` for symbol metadata such as name, exchange, currency, industry, and market capitalization when available.
- Use Finnhub `/stock/market-holiday?exchange=US` for US market-calendar support.
- Do not use Finnhub metrics, earnings, company news, or websocket streaming in this MVP.
- Limit the MVP to US-listed stocks and ETFs.
- Represent broad US indexes through tradable ETF proxies instead of direct index symbols:
  - Nasdaq 100 uses QQQ instead of `^NDX`.
  - S&P 500 uses SPY instead of `^GSPC`.
  - Dow Jones Industrial Average uses DIA instead of `^DJI`.
- Read the fixed Watchlist from environment settings.
- Use AAPL, NVDA, and TSLA as the default local verification Watchlist.
- Cap the fixed Watchlist and dashboard request handling at 20 symbols.
- Normalize Watchlist symbols to uppercase and de-duplicate them before provider calls.
- Reject configured Watchlists or requests above 20 symbols at the Price Snapshot service/API boundary in the fixed-env MVP.
- Later editable Watchlist management should enforce the same 20-symbol limit at the add/update boundary before symbols can enter the Watchlist.
- Add a dashboard-oriented backend endpoint for Watchlist Price Snapshots.
- Return successful Price Snapshot items to the dashboard.
- Treat Finnhub invalid-symbol quote responses with zero price and zero timestamp as unavailable.
- Invalid or unavailable symbols should not break the whole successful response when at least one symbol succeeds.
- Log unavailable symbols and provider failures for diagnosis.
- Use owner-only display assumptions because Finnhub free usage is personal-use oriented.
- Fetch Price Snapshots on dashboard demand rather than through a scheduler.
- Do not store Price Snapshots in Postgres in this MVP.
- Do not use OpenRouter or AI for Price Snapshots.
- Add a Finnhub provider adapter as the external-service boundary.
- Add a Price Snapshot service as the main deep module that coordinates Watchlist validation, cache lookup, provider calls, stale fallback, response shaping, and provider-error handling.
- Define caching behind a small Price Snapshot cache interface.
- Implement the MVP cache as an application-scoped in-process TTL cache.
- Keep the cache interface narrow enough that Redis can later replace the in-process implementation without changing provider, service, API, or dashboard contracts.
- Cache quote data as fresh for 60 seconds.
- Keep quote stale fallback data for up to five minutes when Finnhub is temporarily unavailable or rate-limited.
- Cache profile data for 24 hours.
- Cache US market holiday data for 24 hours or until the next local market-calendar refresh boundary.
- Keep an internal provider rate guard below Finnhub's free-tier 60 API calls per minute.
- Prefer cache hits over provider calls for repeated dashboard refreshes.
- Dashboard should use a compact table-like layout on desktop.
- Dashboard should use compact stacked rows on mobile while preserving the same scan order.
- Dashboard rows should include symbol, name, exchange, currency, current price, previous close, change, change percent, day open, day high, day low, provider, freshness, and last updated time where available.
- Dashboard should show market movement states with the existing market-up, market-down, and market-neutral design tokens.
- Dashboard should show stale freshness when a quote comes from stale fallback data.
- Dashboard should not auto-refresh in the MVP; use manual refresh and respect cache TTL.
- Do not introduce a broad reusable DataTable abstraction in the MVP unless repeated table behavior already exists in the web codebase.
- Keep the implementation consistent with the existing FastAPI service/provider pattern, pydantic-settings configuration, and Next.js dashboard design contract.

## Testing Decisions

- Tests should verify external behavior and stable service contracts, not private implementation details.
- Finnhub provider tests should use mocked HTTP responses for quote, profile, market-holiday, invalid-symbol, provider-error, and rate-limit behavior.
- Price Snapshot service tests should cover symbol normalization, de-duplication, 20-symbol limit enforcement, cache hits, provider fetches, stale fallback, unavailable symbols, and partial success behavior.
- Cache tests should cover fresh TTL, stale fallback TTL, expired entries, and clock-controlled behavior.
- API tests should cover the Watchlist endpoint response shape, successful dashboard payloads, configured Watchlist limit failures, provider failure mapping, and invalid symbol skipping.
- Settings tests should cover `FINNHUB_API_KEY`, fixed Watchlist parsing, uppercase normalization, and default `AAPL,NVDA,TSLA` behavior.
- Dashboard tests should cover loading, empty or unavailable, ready rows, market movement styling, stale freshness display, and manual refresh behavior where the existing web test setup supports it.
- Live Finnhub integration tests should remain opt-in and marked as integration tests; they should skip when `FINNHUB_API_KEY` is missing.
- Default backend tests must not require live Finnhub, Redis, Docker, Telegram, OpenRouter, or a paid provider account.
- Test prior art includes existing backend unit tests for settings, provider-like HTTP boundaries, service behavior, API contracts, and existing dashboard remote-resource rendering patterns.

## Out of Scope

- Editable Watchlist CRUD.
- Watchlist persistence in Postgres.
- Price Snapshot persistence in Postgres.
- Price history storage.
- Line charts, sparklines, intraday charts, historical charts, or technical indicators.
- Direct market index snapshots.
- Korean stocks or Korean ETFs.
- Price alerts, thresholds, or Urgent Alerts.
- Routine Briefing integration.
- Telegram `/price` or `/prices` commands.
- Scheduled price collection or scheduled price pushes.
- Finnhub websocket streaming.
- Finnhub metrics, earnings, company news, insider data, or analyst estimates.
- Paid provider integration.
- Multi-provider fallback.
- AI-generated price explanation, Market Questions, or Investment Analysis.
- Public or commercial redistribution of Finnhub data.

## Further Notes

- This PRD follows `CONTEXT.md`, especially the distinction between **Market Source**, **Watchlist**, **Price Snapshot**, **Interactive Bot**, **Routine Briefing**, **Urgent Alert**, **Market Question**, and **Investment Analysis**.
- The MVP intentionally uses dashboard-demand fetching instead of scheduled collection: each dashboard request decides whether to return fresh cached data, call Finnhub for missing or expired data, or return stale cached data when Finnhub is temporarily unavailable.
- The fixed Watchlist is a delivery shortcut, not the final Watchlist model. The future editable Watchlist should keep the same Price Snapshot contract while moving add/remove behavior into the dashboard and backend validation.
- The in-process cache is intentionally small and replaceable. Redis should be considered only when multi-worker production behavior or shared stale fallback becomes necessary.
- The dashboard table is a product decision, but the MVP should avoid over-building a generic table framework before repeated table behavior exists.
