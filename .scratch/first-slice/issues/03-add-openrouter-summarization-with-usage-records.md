Status: done
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

## Implementation decisions

- Use `AIModel.OPENAI_GPT_4_1_NANO` for `openai/gpt-4.1-nano`.
- Use `AIModel.GOOGLE_GEMINI_2_5_FLASH_LITE` for `google/gemini-2.5-flash-lite`.
- Route `AIFeature.GEEKNEWS_SUMMARY` through OpenRouter with `models: ["openai/gpt-4.1-nano", "google/gemini-2.5-flash-lite"]`.
- Use OpenRouter-managed fallback rather than app-level retry logic.
- Record one AI usage row per TrendBoda AI request; OpenRouter internal fallback attempts are not separate TrendBoda requests.
- Store the response `model` as the actual OpenRouter model string and calculate estimated cost from that model's request-time pricing snapshot.
- Read the OpenRouter API key from `OPENROUTER_API_KEY`.
- Fetch model pricing from OpenRouter `/api/v1/models` and cache it for roughly one day.
- Do not block summarization when `/api/v1/models` lookup fails; use local fallback pricing or mark estimated cost unavailable.
- Store one current summary per GeekNews item; repeated generation upserts and replaces the stored summary for that item.
- Keep every summarization attempt as a separate AI usage record, even when the stored summary is replaced.

## Blocked by

- .scratch/first-slice/issues/02-collect-and-display-geeknews-items.md
- .scratch/first-slice/issues/07-harden-geeknews-slice-and-api-boundaries.md
- .scratch/first-slice/issues/08-standardize-web-tooling-with-pnpm-and-tailwind.md
