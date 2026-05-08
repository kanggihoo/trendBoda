# Provider adapters with cache and fallback

TrendBoda will access external market, disclosure, news, and AI services through provider adapters rather than binding domain logic directly to one API. We chose this because early providers such as yfinance, Polygon/Massive, Finnhub, SEC EDGAR, OpenDART, RSS feeds, and OpenRouter have different reliability, quotas, schemas, and costs, so the system needs cache, fallback, and provider replacement as first-class behavior.

## Consequences

- Domain workflows depend on normalized provider results, not vendor response shapes.
- Provider health, rate limits, and freshness must be tracked because fallback decisions are part of product behavior.
- MVP implementation is slightly slower, but later provider swaps are cheaper and safer.
