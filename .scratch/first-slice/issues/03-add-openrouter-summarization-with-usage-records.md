Status: ready-for-agent
Type: AFK

# Add OpenRouter summarization with usage records

## Parent

.scratch/first-slice/PRD.md

## What to build

Add OpenRouter-powered summarization for stored GeekNews items, using explicit AI feature and model routing with primary and fallback models. The completed slice should let the Owner generate and view stored summaries while every AI request records token usage, estimated cost, latency, status, actual model string, and pricing metadata.

## User stories covered

- 10. Summarize selected GeekNews items with OpenRouter
- 11. Store AI summaries
- 12. Link summaries back to source items
- 13. Record AI usage for every summary request
- 14. Record failed AI requests when possible
- 15. Estimate OpenRouter cost from usage and pricing snapshots
- 21. Use explicit AI feature and model enums
- 22. Support primary and fallback model routing
- 23. Store actual OpenRouter model string
- 24. Store pricing metadata per request
- 27. Expose summary APIs
- 39. Test routing, gateway, cost, storage, API, and dashboard behavior

## Acceptance criteria

- [ ] AI feature and model enums exist for GeekNews summarization and configured model routes.
- [ ] OpenRouter calls go through a gateway that normalizes response content, usage, latency, status, errors, and actual model string.
- [ ] Primary and fallback model behavior is implemented according to feature routing config.
- [ ] Summaries are stored and linked to the source GeekNews item.
- [ ] AI usage records are written for successful requests and failed requests when possible.
- [ ] Estimated cost is calculated from prompt and completion token usage using request-time pricing metadata.
- [ ] FastAPI exposes endpoints to generate and retrieve GeekNews summaries.
- [ ] The dashboard can show a stored summary for a GeekNews item.
- [ ] OpenRouter gateway tests mock HTTP responses and cover success, failure, usage extraction, latency recording, and fallback behavior.
- [ ] Cost calculation tests cover prompt/completion pricing, missing usage fields, zero-token responses, failed requests, and pricing snapshot persistence.
- [ ] AI routing tests cover feature-to-model mapping, config override behavior, and actual model string persistence.

## Blocked by

- .scratch/first-slice/issues/02-collect-and-display-geeknews-items.md
