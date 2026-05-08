Status: ready-for-agent

# TrendBoda First Slice PRD

## Problem Statement

The Owner wants TrendBoda to become a personal briefing system, but the full vision includes many difficult integrations: market prices, disclosures, news, Telegram, dashboard UI, AI cost tracking, and later cloud operations. Building all of that at once would make it hard to validate the core loop. The first implementation needs a small but real source that can prove TrendBoda can collect a Source, turn useful items into Signals, summarize them with OpenRouter, track AI cost, and show results through both the web dashboard and the Interactive Bot.

## Solution

Build the first end-to-end slice around GeekNews RSS. TrendBoda will fetch and parse GeekNews RSS, store items with duplicate prevention, summarize selected items through OpenRouter, record AI usage and estimated cost, expose the data through FastAPI, show it in a Next.js dashboard, and support Telegram commands for recent GeekNews items and OpenRouter cost.

This slice intentionally avoids market data, disclosures, cloud deployment, OpenTofu, and the Rust Ops CLI. It validates the core Source-to-Signal-to-briefing loop locally with Dockerized Postgres, uv-managed host-run FastAPI, and host-run Next.js.

## User Stories

1. As the Owner, I want TrendBoda to fetch GeekNews RSS, so that I can validate Source collection with a real external feed.
2. As the Owner, I want TrendBoda to parse GeekNews RSS items into normalized records, so that the rest of the system does not depend on RSS XML shape.
3. As the Owner, I want TrendBoda to store GeekNews items in Postgres, so that fetched items persist across local runs.
4. As the Owner, I want TrendBoda to prevent duplicate GeekNews items, so that repeated fetches do not pollute the dashboard.
5. As the Owner, I want TrendBoda to record when GeekNews was fetched, so that I can tell whether collection is working.
6. As the Owner, I want to see recent GeekNews items in the dashboard, so that I can browse developer trend information from one place.
7. As the Owner, I want to open the original GeekNews item from the dashboard, so that I can inspect the source article.
8. As the Owner, I want to see item publish time and fetch time, so that I can judge freshness.
9. As the Owner, I want to trigger a GeekNews fetch manually during local development, so that I can test the collector without waiting for a scheduler.
10. As the Owner, I want TrendBoda to summarize selected GeekNews items with OpenRouter, so that I can quickly understand what matters.
11. As the Owner, I want AI summaries to be stored, so that summaries are reusable and not regenerated unnecessarily.
12. As the Owner, I want summaries to link back to source items, so that I can verify AI output against the original content.
13. As the Owner, I want AI usage recorded for every summary request, so that cost tracking is not optional or forgotten.
14. As the Owner, I want failed AI requests recorded when possible, so that the AI Cost Dashboard reflects reliability as well as spend.
15. As the Owner, I want TrendBoda to estimate OpenRouter cost from token usage and pricing snapshots, so that historical cost numbers stay stable.
16. As the Owner, I want AI cost grouped by date, so that I can see daily spend.
17. As the Owner, I want AI cost grouped by model, so that I can compare model expense.
18. As the Owner, I want AI cost grouped by feature, so that I can see which TrendBoda behavior spends money.
19. As the Owner, I want request-level AI usage detail, so that I can inspect latency, status, tokens, and cost for a specific request.
20. As the Owner, I want monthly budget progress, so that I can avoid runaway OpenRouter spend.
21. As the Owner, I want AI model routing to use explicit feature and model enums, so that model changes are intentional.
22. As the Owner, I want model routing to support primary and fallback models, so that a model failure does not break summaries when a fallback is configured.
23. As the Owner, I want the actual OpenRouter model string stored per request, so that dashboard data matches what was really used.
24. As the Owner, I want pricing metadata stored per request, so that later pricing changes do not rewrite the past.
25. As the Owner, I want the FastAPI backend to expose health checks, so that local development and future operations can verify service status.
26. As the Owner, I want the FastAPI backend to expose GeekNews item APIs, so that the dashboard and bot can read the same data.
27. As the Owner, I want the FastAPI backend to expose summary APIs, so that summaries can be generated and displayed consistently.
28. As the Owner, I want the FastAPI backend to expose AI cost APIs, so that the dashboard and bot can show usage.
29. As the Owner, I want the Next.js dashboard to show GeekNews items and summaries, so that web viewing is useful from day one.
30. As the Owner, I want the Next.js dashboard to show OpenRouter cost metrics, so that spend is visible without opening Grafana.
31. As the Owner, I want Telegram `/geeknews`, so that I can view recent GeekNews items from my phone.
32. As the Owner, I want Telegram `/cost`, so that I can check OpenRouter spend from my phone.
33. As the Owner, I want Telegram responses to be concise, so that messages are readable on mobile.
34. As the Owner, I want long source details kept in the dashboard, so that Telegram stays lightweight.
35. As the Owner, I want local Postgres to run through Docker Compose, so that the database environment is reproducible.
36. As the Owner, I want FastAPI to run directly on the host through uv and Next.js to run directly on the host during development, so that hot reload and debugging stay simple.
37. As the Owner, I want schema changes managed by dbmate, so that database changes are versioned.
38. As the Owner, I want repository classes to be the only Python-to-database boundary, so that SQL remains organized without SQLAlchemy.
39. As the Owner, I want tests for parser, storage, AI routing, cost calculation, API contracts, dashboard behavior, and Telegram formatting, so that future market-data work can build on a reliable base.
40. As the Owner, I want market data and disclosure work excluded from this slice, so that this first implementation stays focused and shippable.

## Implementation Decisions

- Build around GeekNews RSS as the first Developer Trend Source because it has no API key requirement and exercises the collection, storage, AI, dashboard, and bot loop.
- Use provider adapters with normalized results. The GeekNews RSS adapter returns stable application-level item data rather than exposing feed XML details.
- Store GeekNews items with duplicate prevention based on a stable external identifier, preferring feed GUID when present and source URL when needed.
- Record fetch runs separately from items so provider health and freshness can be inspected later.
- Use FastAPI for the backend and asyncpg for Postgres access.
- Use uv for Python dependency management and backend command execution.
- Use repository classes as the database boundary. Application services do not build ad hoc SQL outside repositories.
- Use dbmate migrations with explicit `migrate:up` and `migrate:down` SQL sections.
- Run local Postgres through Docker Compose while FastAPI and Next.js run on the host.
- Use OpenRouter only for summarization in this slice, not for raw RSS listing or deterministic status views.
- Implement an OpenRouter gateway that normalizes request, response, token usage, latency, status, errors, and actual model string.
- Represent AI features and models with enums, then route each feature to primary and fallback models through config.
- Store AI usage records for successful and failed requests when possible.
- Calculate estimated cost from response token usage and a request-time pricing snapshot.
- Store prompt tokens, completion tokens, total tokens, model, feature, latency, status, estimated cost, pricing metadata, and request timestamp.
- Store summaries separately from AI usage records and link summaries to source items and usage records.
- The GeekNews summary feature uses the AI feature route for developer-trend summaries.
- The AI Cost Dashboard groups OpenRouter usage by date, model, feature, request, and monthly budget progress.
- The Next.js dashboard is the product UI for browsing GeekNews and cost data. Grafana remains out of scope for this slice.
- The Telegram Interactive Bot starts with polling for local development.
- Telegram `/geeknews` returns a concise list of recent GeekNews items and may include short stored summaries when available.
- Telegram `/cost` returns concise OpenRouter spend and usage metrics.
- Cloud deployment, domain-backed HTTPS, Caddy, OpenTofu, and the Rust Ops CLI remain planned later work, not first-slice requirements.

## Testing Decisions

- Tests should verify external behavior and stable module contracts, not private implementation details.
- GeekNews RSS parser tests should cover valid RSS, missing optional fields, HTML entities, duplicate identifiers, item ordering, and malformed XML failure behavior.
- GeekNews provider adapter tests should use fixture XML rather than live network calls.
- Repository tests should cover item insertion, duplicate prevention, fetch run recording, summary storage, AI usage storage, and cost aggregation queries.
- Service tests should cover fetch orchestration, summarize orchestration, idempotency, and error handling.
- OpenRouter gateway tests should mock HTTP responses and cover successful usage extraction, failed responses, latency recording, and fallback model behavior.
- AI routing tests should verify feature-to-model mapping, env/config override behavior, and actual model string persistence.
- Cost calculation tests should cover prompt/completion pricing, missing usage fields, zero-token responses, failed requests, and pricing snapshot persistence.
- FastAPI tests should cover health, GeekNews list/fetch/summarize endpoints, AI cost endpoints, validation errors, and no-network test mode.
- Dashboard tests should cover rendering GeekNews items, summary display, empty states, loading states, error states, cost grouping, and budget progress display.
- Telegram command tests should treat formatting as pure behavior and cover `/geeknews`, `/cost`, empty results, and backend error responses.
- Local development smoke tests should verify Postgres starts, uv can run backend commands, migrations apply, API health returns OK, and dashboard can call the API.

## Out of Scope

- Stock prices and Price Snapshots
- Market Sources
- Disclosure Sources
- SEC EDGAR integration
- OpenDART integration
- GitHub trend collection
- Market Questions
- Investment Analysis
- Routine Briefings beyond GeekNews command-style output
- Urgent Alerts
- Cloud deployment to EC2
- Domain purchase or DNS setup
- Caddy HTTPS reverse proxy
- Vercel deployment
- Grafana Cloud integration
- OpenTofu infrastructure code
- Rust Ops CLI
- Multi-owner support
- Auth beyond local-owner assumptions
- Full natural-language Telegram conversation

## Further Notes

- This PRD follows `CONTEXT.md`, especially the distinction between TrendBoda, Owner, Source, Developer Trend Source, Signal, Interactive Bot, AI Cost Dashboard, and Price Snapshot.
- This PRD respects ADR-0001 through ADR-0008, but implements only the local first-slice subset.
- The first slice should create enough structure that market data and disclosures can later reuse provider adapters, repositories, AI usage tracking, dashboard patterns, and Telegram command patterns.
- The issue tracker source of truth is local markdown under `.scratch/`.
