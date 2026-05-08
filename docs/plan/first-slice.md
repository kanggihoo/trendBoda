# First Slice

The first TrendBoda implementation slice validates the core loop before market data, disclosures, GitHub trends, cloud deployment, or the Rust operations CLI are added.

## Scope

- Fetch and parse GeekNews RSS from `https://feeds.feedburner.com/geeknews-feed`
- Store GeekNews items with duplicate prevention
- Summarize selected items through OpenRouter
- Track OpenRouter usage, estimated cost, latency, status, model, and feature
- Show GeekNews items and summaries in the web dashboard
- Show OpenRouter cost data in the web dashboard
- Support Telegram `/geeknews` and `/cost`
- Run locally with Dockerized Postgres, uv-managed host-run FastAPI, and host-run Next.js

## Out of Scope

- Stock prices and price snapshots
- SEC EDGAR and OpenDART disclosures
- GitHub trend collection
- EC2 deployment
- Caddy and domain-backed HTTPS
- OpenTofu infrastructure code
- Rust operations CLI

## Implementation Order

1. Create FastAPI, Next.js, uv, and local Postgres project structure.
2. Add dbmate migrations for GeekNews items and AI usage.
3. Implement GeekNews RSS provider adapter.
4. Implement OpenRouter adapter with AI feature/model routing.
5. Persist summaries and AI usage records.
6. Add API endpoints for GeekNews items, summaries, and AI cost metrics.
7. Build dashboard pages for GeekNews and AI cost.
8. Add Telegram commands for `/geeknews` and `/cost`.
