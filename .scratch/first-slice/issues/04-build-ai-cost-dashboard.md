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

- [ ] FastAPI exposes AI cost summary endpoints grouped by date, model, and feature.
- [ ] FastAPI exposes request-level AI usage detail for recent requests.
- [ ] Monthly budget progress is calculated from configured budget and estimated monthly cost.
- [ ] Dashboard shows cost summary cards, grouping views, request details, latency, error status, and budget progress.
- [ ] Empty states are clear when no OpenRouter requests have been recorded.
- [ ] Error states are handled when cost APIs fail.
- [ ] Repository tests cover AI usage aggregation queries.
- [ ] API tests cover summary, detail, empty, and validation behavior.
- [ ] Dashboard tests cover rendering, loading, empty, error, grouping, and budget progress behavior.

## Blocked by

- .scratch/first-slice/issues/03-add-openrouter-summarization-with-usage-records.md
- .scratch/first-slice/issues/08-standardize-web-tooling-with-pnpm-and-tailwind.md
