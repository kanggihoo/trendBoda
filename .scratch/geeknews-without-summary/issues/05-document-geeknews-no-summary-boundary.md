Status: done
Type: AFK

# Document GeekNews No-Summary Boundary

## Parent

.scratch/geeknews-without-summary/PRD.md

## What to build

Update stale project wording so future agents understand that GeekNews is a Developer Trend Source producing GeekNews Signals for scanning and link navigation, not a default AI summary input. Documentation and issue wording should preserve the broader TrendBoda AI foundation while clearly excluding automatic GeekNews summarization from the default owner flow.

## User stories covered

- 13. Document the GeekNews boundary clearly for future agents

## Acceptance criteria

- [x] First-slice or related issue wording no longer says the default GeekNews owner flow requires automatic summarization.
- [x] Documentation uses `GeekNews Signal`, `GeekNews Provider`, and `GeekNews Item Content` terminology consistently with `CONTEXT.md`.
- [x] Documentation states OpenRouter-backed AI remains available outside the default GeekNews flow.
- [x] Removed GeekNews summary endpoints are documented as outside the default public API surface.
- [x] No parent PRD is closed or modified as part of publishing this issue.

## Blocked by

- .scratch/geeknews-without-summary/issues/01-serve-geeknews-signals-without-summary-dependency.md
- .scratch/geeknews-without-summary/issues/02-render-dashboard-geeknews-signals-without-summary-ui.md
- .scratch/geeknews-without-summary/issues/03-return-concise-geeknews-interactive-bot-output.md
- .scratch/geeknews-without-summary/issues/04-preserve-openrouter-foundation-and-ai-cost-dashboard.md
