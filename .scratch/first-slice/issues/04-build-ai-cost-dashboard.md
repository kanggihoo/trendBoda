Status: ready-for-agent
Type: AFK

# Build AI Cost Dashboard

## Parent

.scratch/first-slice/PRD.md

## What to build

Build the product-facing AI Cost Dashboard for OpenRouter usage. The Owner should be able to see estimated cost and usage grouped by date, model, feature, request, latency, error status, and monthly budget progress from the web dashboard, without needing Grafana for product-level spend visibility.

## User stories covered

- 16. See AI cost grouped by date
- 17. See AI cost grouped by model
- 18. See AI cost grouped by feature
- 19. Inspect request-level AI usage detail
- 20. See monthly budget progress
- 28. Expose AI cost APIs
- 30. Show OpenRouter cost metrics in the dashboard
- 39. Test cost aggregation, API, and dashboard behavior

## Acceptance criteria

- [x] FastAPI exposes AI cost summary endpoints grouped by date, model, and feature.
- [x] FastAPI exposes request-level AI usage detail for recent requests.
- [x] Monthly budget progress is calculated from configured budget and estimated monthly cost.
- [x] Dashboard shows cost summary cards, grouping views, request details, latency, error status, and budget progress.
- [x] Empty states are clear when no OpenRouter requests have been recorded.
- [x] Error states are handled when cost APIs fail.
- [x] Repository tests cover AI usage aggregation queries.
- [x] API tests cover summary, detail, empty, and validation behavior.
- [x] Dashboard tests cover rendering, loading, empty, error, grouping, and budget progress behavior.

## Implementation decisions

- Treat local AI usage records as the primary product-facing cost source.
- Use OpenRouter `/api/v1/credits` and `/api/v1/activity` only for audit and reconciliation views, because they require a separate management key.
- Read the OpenRouter management key from `OPENROUTER_API_MANAGEMENT_KEY`.
- Do not require the management key for the first cost dashboard; show local estimated cost even when audit endpoints are unavailable.
- Defer OpenRouter account audit and reconciliation to `.scratch/first-slice/issues/12-add-openrouter-account-audit-reconciliation.md`.
- Use `AI_MONTHLY_BUDGET_USD=10.00` as the first-slice monthly AI budget.

## Blocked by

- .scratch/first-slice/issues/03-add-openrouter-summarization-with-usage-records.md
- .scratch/first-slice/issues/08-standardize-web-tooling-with-pnpm-and-tailwind.md
