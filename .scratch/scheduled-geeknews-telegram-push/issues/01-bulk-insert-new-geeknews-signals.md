Status: done
Type: AFK

# Bulk Insert New GeekNews Signals

## Parent

.scratch/scheduled-geeknews-telegram-push/PRD.md

## What to build

Change GeekNews item persistence so each fetch stores new GeekNews Signals with a bulk insert path instead of one database roundtrip per item. The fetch flow should still parse the full current RSS feed, rely on the existing GeekNews identity for duplicate prevention, preserve existing item snapshots, and return the newly inserted stored items for later Telegram push.

## Acceptance criteria

- [ ] GeekNews RSS fetch behavior still parses every item returned by the current feed.
- [ ] GeekNews item persistence uses one bulk insert operation where practical instead of per-item execute calls.
- [ ] Duplicate GeekNews items are ignored through database conflict handling.
- [ ] Duplicate handling uses `ON CONFLICT DO NOTHING` or equivalent insert-ignore behavior.
- [ ] Existing GeekNews item rows are not rewritten by routine duplicate fetches.
- [ ] Existing item title, content, fetched time, and updated time remain unchanged after duplicate fetches.
- [ ] The repository returns a result containing inserted count and newly inserted stored GeekNews items.
- [ ] The manual fetch API can still report inserted count.
- [ ] Repository tests cover bulk insert, duplicate prevention, unchanged existing rows, and returned newly inserted items.

## Blocked by

None - can start immediately
