Status: done
Type: AFK

# Return Concise GeekNews Interactive Bot Output

## Parent

.scratch/geeknews-without-summary/PRD.md

## What to build

Update the Interactive Bot `/geeknews` owner flow so Telegram output returns concise GeekNews Signals from the shared backend source without AI-generated summary text. Mobile messages should prioritize item title, short description, publish time or fetch freshness where useful, and links.

## User stories covered

- 3. Return concise Telegram `/geeknews` output without AI-generated text
- 4. Keep GeekNews links prominent
- 6. Keep dashboard and Interactive Bot sharing one backend source
- 14. Prove GeekNews still displays items without summaries

## Acceptance criteria

- [x] `/geeknews` output uses stored GeekNews Signals from the backend item source.
- [x] Telegram messages include concise item text and links without AI summary text or summary-specific wording.
- [x] Missing summary data does not change `/geeknews` into an error, fallback, or incomplete response.
- [x] Empty and error messages remain concise and appropriate for the Interactive Bot.
- [x] Formatter or bot tests verify `/geeknews` output contains item text and links without AI summary text.

## Blocked by

- .scratch/geeknews-without-summary/issues/01-serve-geeknews-signals-without-summary-dependency.md
