Status: done
Type: AFK

# Preserve OpenRouter Foundation And AI Cost Dashboard

## Parent

.scratch/geeknews-without-summary/PRD.md

## What to build

Keep the OpenRouter-backed AI foundation intact while removing GeekNews summary behavior from the default GeekNews owner flow. OpenRouter configuration, AI feature and model routing, AI usage records, pricing snapshots, historical usage readability, and the AI Cost Dashboard should remain available for future AI-backed TrendBoda features.

## User stories covered

- 9. Keep OpenRouter settings and AI model routing intact
- 10. Keep the AI Cost Dashboard available
- 11. Keep historical AI usage records readable

## Acceptance criteria

- [x] OpenRouter gateway, model routing, pricing snapshots, and AI usage record behavior remain available for non-GeekNews AI-backed features.
- [x] AI Cost Dashboard still loads and displays empty, populated, and error states from local AI usage data.
- [x] Historical AI usage records remain readable even if older records reference GeekNews summary experiments.
- [x] Tests for AI routing, OpenRouter usage recording, cost aggregation, and AI Cost Dashboard remain valid unless only GeekNews-summary-specific assertions need updating.
- [x] This slice does not remove broad AI tables, settings, routing enums, or cost dashboard surfaces.

## Blocked by

- .scratch/geeknews-without-summary/issues/01-serve-geeknews-signals-without-summary-dependency.md
