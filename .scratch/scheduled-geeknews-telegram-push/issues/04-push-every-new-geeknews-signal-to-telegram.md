Status: done
Type: AFK

# Push Every New GeekNews Signal To Telegram

## Parent

.scratch/scheduled-geeknews-telegram-push/PRD.md

## What to build

Connect the scheduled GeekNews job to Telegram push for newly inserted GeekNews Signals. Every newly inserted Signal should be sent as its own Telegram message using the existing Telegram configuration and sender. Telegram send failures should be isolated per message so later new Signals are still attempted in the same run.

## Acceptance criteria

- [ ] Every newly inserted GeekNews Signal is attempted as an individual Telegram message.
- [ ] Scheduled Telegram push has no count limit or batching policy in this slice.
- [ ] Telegram messages use concise GeekNews Signal formatting with title, useful text, and source link data.
- [ ] Telegram read and unread state is left to the Telegram client; TrendBoda does not store read state.
- [ ] Telegram push uses newly inserted stored items returned by repository behavior, not a timestamp-only query.
- [ ] One Telegram message failure does not stop attempts for later new GeekNews Signals in the same run.
- [ ] Telegram push failures do not roll back successful GeekNews DB inserts.
- [ ] The job logs attempted push count, successful push count, failed push count, and item-level failure context.
- [ ] No delivery tracking table or automatic retry queue is introduced.
- [ ] Tests cover all-new-item push, per-message failure isolation, total failure logging, and no delivery storage dependency.

## Blocked by

- .scratch/scheduled-geeknews-telegram-push/issues/03-run-scheduled-geeknews-fetch-once.md
