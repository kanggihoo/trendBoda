Status: ready-for-agent

# Harden Finnhub Price Snapshot Provider

## Parent

.scratch/us-price-snapshot-dashboard/PRD.md

## What to build

Build the first Finnhub provider boundary for US Price Snapshots and prove it can normalize Finnhub quote, profile, and US market-holiday responses into stable TrendBoda data shapes. This slice should make Finnhub behavior testable without requiring live network calls in default tests, while keeping opt-in live integration coverage available when `FINNHUB_API_KEY` is configured.

## Acceptance criteria

- [ ] Finnhub `/quote` responses are normalized into a Price Snapshot provider result with current price, previous close, change, change percent, open, high, low, and provider timestamp.
- [ ] Finnhub `/stock/profile2` responses are normalized into symbol metadata including name, exchange, currency, industry, and market capitalization where available.
- [ ] Finnhub `/stock/market-holiday?exchange=US` responses are normalized into US market-calendar support data.
- [ ] Invalid quote responses with zero price and zero timestamp are represented as unavailable rather than successful Price Snapshots.
- [ ] Provider failures, unauthorized responses, and rate-limit responses are represented through explicit provider errors that services can handle.
- [ ] Unit tests use mocked HTTP responses for quote, profile, holiday, invalid symbol, provider failure, unauthorized, and rate-limit behavior.
- [ ] Live Finnhub integration tests remain opt-in, are marked as integration tests, and skip when `FINNHUB_API_KEY` is missing.
- [ ] Default backend tests do not require live Finnhub, Redis, Docker, Telegram, OpenRouter, or a paid provider account.

## Blocked by

None - can start immediately
