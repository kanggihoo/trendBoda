Status: ready-for-agent
Type: AFK

# Add Telegram Interactive Bot commands

## Parent

.scratch/first-slice/PRD.md

## What to build

Add the first Telegram Interactive Bot commands for the first slice. The Owner should be able to run the bot locally with polling, ask for recent GeekNews items with `/geeknews`, and check OpenRouter cost with `/cost`. Telegram responses should stay concise and mobile-friendly, leaving long details for the dashboard.

## User stories covered

- 31. Telegram `/geeknews`
- 32. Telegram `/cost`
- 33. Concise Telegram responses
- 34. Keep long details in the dashboard
- 39. Test Telegram formatting and backend error behavior

## Acceptance criteria

- [ ] Telegram bot can run locally in polling mode.
- [ ] `/geeknews` returns a concise list of recent GeekNews items and includes stored summaries when available.
- [ ] `/cost` returns concise OpenRouter spend and usage metrics.
- [ ] Telegram responses include dashboard links or source links where appropriate without becoming long-form reports.
- [ ] Empty states are handled when no GeekNews items or AI usage records exist.
- [ ] Backend/API failures are handled with clear Telegram messages.
- [ ] Telegram command formatting is covered by pure-function tests.
- [ ] Command handler tests cover `/geeknews`, `/cost`, empty results, and backend error responses.

## Blocked by

- .scratch/first-slice/issues/02-collect-and-display-geeknews-items.md
- .scratch/first-slice/issues/07-harden-geeknews-slice-and-api-boundaries.md
- .scratch/first-slice/issues/04-build-ai-cost-dashboard.md
