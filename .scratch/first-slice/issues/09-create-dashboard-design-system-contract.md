Status: needs-info
Type: AFK

# Create dashboard design system contract

## Parent

.scratch/first-slice/PRD.md

## What to build

Create a root `DESIGN.md` that defines the visual system contract for TrendBoda web dashboard work. The file should give future agents a clear source of truth for dashboard tone, typography, colors, spacing, radius, icons, Tailwind usage, shadcn/ui usage, and component-level visual conventions.

This issue is intentionally marked `needs-info` until the exact visual direction and token set are clarified. Do not start implementation until the design contract scope is resolved.

## User stories covered

- 29. Show GeekNews items in the Next.js dashboard
- 30. Show OpenRouter cost metrics in the dashboard
- 39. Test parser, storage, API, and dashboard behavior

## Open questions

- What visual tone should TrendBoda use beyond "quiet operational dashboard"?
- What base color palette should become the first dashboard token set?
- What density level should repeated dashboard views use?
- What shadcn/ui components should be part of the first allowed set?
- What component states must be defined first: loading, empty, error, success, warning, disabled?
- Should `DESIGN.md` follow the Google Labs `design.md` structure exactly, or use a smaller repo-local subset first?
- Should design tokens be exportable to Tailwind config in this first pass, or documented only?

## Acceptance criteria

- [ ] Root `DESIGN.md` exists.
- [ ] `DESIGN.md` defines TrendBoda dashboard visual tone.
- [ ] `DESIGN.md` defines Pretendard typography usage.
- [ ] `DESIGN.md` defines initial color, spacing, border, radius, and state tokens.
- [ ] `DESIGN.md` defines lucide icon usage rules.
- [ ] `DESIGN.md` defines shadcn/ui usage rules.
- [ ] `DESIGN.md` defines Tailwind application guidance for the dashboard.
- [ ] `DESIGN.md` is referenced from `docs/agents/web.md`.
- [ ] The design contract avoids adding product features or broad component abstractions.

## Blocked by

- Clarify the open design questions above.
