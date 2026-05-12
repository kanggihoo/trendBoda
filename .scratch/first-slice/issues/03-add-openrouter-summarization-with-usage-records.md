Status: done
Type: AFK

# Add OpenRouter AI foundation with usage records

## Parent

.scratch/first-slice/PRD.md

## What to build

Add the OpenRouter-powered AI foundation, using explicit AI feature and model routing with primary and fallback models. GeekNews summary endpoints are removed from the public default API surface. Every AI request records token usage, estimated cost, latency, status, actual model string, and pricing metadata.

## User stories covered

- 10. Preserve OpenRouter-backed AI foundations outside the default GeekNews owner flow
- 11. Keep historical AI summaries readable
- 12. Keep historical summary data compatible if present
- 13. Record AI usage for every AI request
- 14. Record failed AI requests when possible
- 15. Estimate OpenRouter cost from usage and pricing snapshots
- 21. Use explicit AI feature and model enums
- 22. Support primary and fallback model routing
- 23. Store actual OpenRouter model string
- 24. Store pricing metadata per request
- 27. Remove GeekNews summary APIs from the default public API surface
- 39. Test routing, gateway, cost, storage, API, and dashboard behavior

## Acceptance criteria

- [x] AI feature and model enums exist for configured OpenRouter routes.
- [x] OpenRouter calls go through a gateway that normalizes response content, usage, latency, status, errors, and actual model string.
- [x] Primary and fallback model behavior is implemented according to feature routing config.
- [x] Historical summary data remains compatible if present.
- [x] AI usage records are written for successful requests and failed requests when possible.
- [x] Estimated cost is calculated from prompt and completion token usage using request-time pricing metadata.
- [x] FastAPI does not expose GeekNews summary endpoints in the default public API surface.
- [x] Historical stored summaries remain readable outside the default GeekNews dashboard flow.
- [x] OpenRouter gateway tests mock HTTP responses and cover success, failure, usage extraction, latency recording, and fallback behavior.
- [x] Cost calculation tests cover prompt/completion pricing, missing usage fields, zero-token responses, failed requests, and pricing snapshot persistence.
- [x] AI routing tests cover feature-to-model mapping, config override behavior, and actual model string persistence.

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
- Keep historical AI usage records readable, including records from older GeekNews summary experiments.

## Blocked by

- .scratch/first-slice/issues/02-collect-and-display-geeknews-items.md
- .scratch/first-slice/issues/07-harden-geeknews-slice-and-api-boundaries.md
- .scratch/first-slice/issues/08-standardize-web-tooling-with-pnpm-and-tailwind.md
