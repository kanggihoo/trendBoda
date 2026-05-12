Status: done
Type: AFK

# Render Dashboard GeekNews Signals Without Summary UI

## Parent

.scratch/geeknews-without-summary/PRD.md

## What to build

Update the dashboard GeekNews owner view so GeekNews Signals are presented for fast scanning and link navigation without automatic or prominent AI summary affordances. The Owner should see title, short description, publish time, fetch time, and links, with loading, empty, and error states that do not imply summary generation.

## User stories covered

- 1. Show GeekNews items without automatic AI summary
- 2. Focus dashboard rows on title, short description, publish time, fetch time, and links
- 4. Keep GeekNews links prominent
- 7. Remove summary buttons, summary panels, and summary loading states
- 14. Prove GeekNews still displays items without summaries

## Acceptance criteria

- [x] Dashboard GeekNews rows render title, short description, publish time, fetch time, and source links without requiring summary data.
- [x] GeekNews summary buttons, panels, loading states, and default summary calls are removed from the dashboard owner flow.
- [x] Dashboard loading, empty, and error states stay specific to GeekNews Signal retrieval rather than summary generation.
- [x] Existing AI Cost Dashboard UI remains available and unchanged except for any copy needed to avoid implying GeekNews summaries are default.
- [x] Dashboard tests cover item rendering without summary UI, loading state, empty state, and error state.

## Blocked by

- .scratch/geeknews-without-summary/issues/01-serve-geeknews-signals-without-summary-dependency.md
