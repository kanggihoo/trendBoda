Status: ready-for-agent

# Remove GeekNews Summary From Default Flow PRD

## Problem Statement

The Owner wants GeekNews to work as a fast Developer Trend Source for scanning titles, short descriptions, and links. The current first-slice direction included OpenRouter-powered summaries for GeekNews items, but GeekNews entries already provide enough context for quick review and link navigation. Automatic or prominent GeekNews summarization adds cost, latency, failure modes, and possible confusion about whether TrendBoda summarized the GeekNews entry or the original linked article.

The Owner still wants OpenRouter configuration, model routing, usage tracking, and the AI Cost Dashboard to remain available for other AI-backed TrendBoda features. The problem is specific to GeekNews: the default GeekNews path should not imply that every GeekNews Signal needs an AI summary.

## Solution

Remove GeekNews summary behavior from the default GeekNews owner flow while preserving the broader OpenRouter and AI usage foundation. GeekNews should fetch RSS, store normalized items, expose stored items through the backend, show them in the dashboard, and return concise Telegram command output focused on title, description, publish time, fetch time, and links.

OpenRouter-backed AI modules, model routing, usage records, and cost dashboard behavior remain in the codebase for future Market Questions, Investment Analysis, Routine Briefings, or other AI-backed TrendBoda features. This PRD should be implemented as a narrow product simplification, not a broad AI subsystem removal.

## User Stories

1. As the Owner, I want GeekNews items to be shown without an automatic AI summary, so that I can scan the original signal quickly.
2. As the Owner, I want GeekNews dashboard rows to focus on title, short description, publish time, fetch time, and links, so that I can decide whether to open the source.
3. As the Owner, I want Telegram `/geeknews` to return concise GeekNews Signals without AI-generated text, so that mobile messages stay lightweight.
4. As the Owner, I want GeekNews links to remain prominent, so that I can move to the GeekNews entry or original source when interested.
5. As the Owner, I want GeekNews RSS fetching and duplicate prevention to remain unchanged, so that existing collection behavior stays reliable.
6. As the Owner, I want stored GeekNews item retrieval to remain unchanged for non-summary fields, so that the dashboard and Interactive Bot keep sharing one backend source.
7. As the Owner, I want summary buttons, summary panels, or summary loading states removed from the GeekNews UI, so that the dashboard does not suggest a feature I do not need.
8. As the Owner, I want GeekNews API behavior to avoid requiring summary data, so that missing summaries are not treated as incomplete items.
9. As the Owner, I want OpenRouter settings and AI model routing to remain intact, so that future AI-backed TrendBoda features do not lose their foundation.
10. As the Owner, I want the AI Cost Dashboard to remain available, so that future OpenRouter usage remains inspectable.
11. As the Owner, I want historical AI usage records to remain readable, so that previous local experiments are not broken by this change.
12. As the Owner, I want this change to avoid broad database churn where possible, so that it stays a small product correction.
13. As a future agent, I want the GeekNews boundary documented clearly, so that I do not reintroduce default GeekNews summarization by following the old first-slice assumptions.
14. As a future agent, I want tests to prove GeekNews still fetches and displays items without summaries, so that the simplified flow remains stable.

## Implementation Decisions

- Treat GeekNews as **GeekNews Signals** for scanning and link navigation, not as automatic AI summary inputs.
- Remove or hide GeekNews-specific summary generation affordances from the dashboard default flow.
- Remove or stop exposing GeekNews-specific summary actions from the owner-facing API surface if those actions are only used by the old GeekNews summary flow.
- Keep GeekNews fetch, item storage, duplicate prevention, fetch run recording, and item retrieval behavior intact.
- Keep OpenRouter gateway, AI feature/model routing, AI usage records, pricing snapshots, and AI Cost Dashboard modules available for non-GeekNews features.
- Do not delete the broader AI foundation as part of this PRD.
- Prefer leaving historical summary database structures in place unless removal is clearly low-risk and covered by migrations. A narrow behavior removal is preferred over destructive schema cleanup.
- Update first-slice or related issue wording where it still says GeekNews requires automatic summarization.
- Use **GeekNews Signal** and **GeekNews Item Content** terminology from `CONTEXT.md`.
- If an existing API contract includes summary fields in GeekNews item responses, those fields may remain optional for backward compatibility, but the default UI and bot output should not depend on them.
- If a GeekNews summary endpoint remains temporarily for compatibility, mark it as not part of the default GeekNews owner flow and avoid linking to it from dashboard or Telegram behavior.

## Testing Decisions

- Tests should verify owner-visible behavior, not private implementation details.
- GeekNews dashboard tests should cover item rendering without summary UI, loading state, empty state, and error state.
- Telegram formatter tests should verify `/geeknews` output contains concise item text and links without AI summary text.
- Backend API tests should verify GeekNews item list/fetch behavior does not require summary data.
- Existing AI routing, OpenRouter gateway, AI usage, and AI Cost Dashboard tests should remain valid unless they were coupled specifically to GeekNews summary behavior.
- If GeekNews summary endpoints are removed, API tests should be updated to reflect the new public contract.
- If GeekNews summary endpoints are kept temporarily, tests should make clear they are not required for the default GeekNews flow.
- No live OpenRouter, live Telegram, or live GeekNews network test should be required for default unit tests.

## Out of Scope

- Removing OpenRouter integration.
- Removing AI model routing.
- Removing AI usage records.
- Removing the AI Cost Dashboard.
- Adding Market Questions or Investment Analysis.
- Adding automatic scheduled GeekNews collection.
- Adding automatic Telegram push delivery.
- Fetching original linked article bodies.
- Building Korean reading notes, AI preview notes, or another replacement GeekNews AI feature.
- Adding authentication or multi-owner permission checks.
- Performing broad database cleanup unrelated to the GeekNews summary behavior.

## Further Notes

- This PRD follows the `CONTEXT.md` decision that GeekNews uses **GeekNews Signals** for scanning and link navigation.
- The decision is intentionally narrower than "remove AI from TrendBoda." AI remains part of TrendBoda; GeekNews no longer needs AI in its default flow.
- The current shape likely requires small UI/API/test adjustments rather than a large architectural refactor.
