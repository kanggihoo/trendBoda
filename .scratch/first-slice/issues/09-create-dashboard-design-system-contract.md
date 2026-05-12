Status: done
Type: AFK

# Create dashboard design system contract

## Parent

.scratch/first-slice/PRD.md

## What to build

Create a root `DESIGN.md` that defines the visual system contract for TrendBoda web dashboard work. The file should give future agents a clear source of truth for dashboard tone, typography, colors, spacing, radius, icons, Tailwind usage, shadcn/ui usage, and component-level visual conventions.

The exact visual direction and token set were clarified in root `DESIGN.md`. This issue is no longer blocked on design direction.

## User stories covered

- 29. Show GeekNews items in the Next.js dashboard
- 30. Show OpenRouter cost metrics in the dashboard
- 39. Test parser, storage, API, and dashboard behavior

## Resolved questions

- Visual tone: light-first, precise, quiet, developer-oriented operational dashboard inspired by Linear structure without copying Linear branding or marketing layout.
- Palette: light default, readable charcoal dark mode, Developer Emerald primary accent, separated semantic and market movement colors.
- Density: medium-high density for repeated dashboard review.
- shadcn/ui scope: Button, Card, Badge, Tabs, Table, Input, Select, DropdownMenu, Dialog, Tooltip, Skeleton, and Alert.
- Component states: loading, empty, ready, success, warning, error, disabled, stale, urgent, plus separate market movement states.
- `DESIGN.md` format: YAML frontmatter for machine-readable tokens plus Markdown body for human guidance.
- Tailwind export: deferred; this issue creates a documented design contract only.

## Acceptance criteria

- [x] Root `DESIGN.md` exists.
- [x] `DESIGN.md` defines TrendBoda dashboard visual tone.
- [x] `DESIGN.md` defines Pretendard typography usage.
- [x] `DESIGN.md` defines initial color, spacing, border, radius, and state tokens.
- [x] `DESIGN.md` defines lucide icon usage rules.
- [x] `DESIGN.md` defines shadcn/ui usage rules.
- [x] `DESIGN.md` defines Tailwind application guidance for the dashboard.
- [x] `DESIGN.md` is referenced from `docs/agents/web.md`.
- [x] The design contract avoids adding product features or broad component abstractions.

## Remaining follow-up

- Apply the `DESIGN.md` tokens to `web/app/globals.css` and dashboard components.
- Wire theme tokens into Tailwind/shadcn when the dashboard styling migration is ready.
- Implement dark mode behavior; it is documented but not yet built.
- Run `npx @google/design.md lint DESIGN.md` later if the project adopts the Google design.md tooling.
