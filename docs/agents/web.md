# Web Agent Notes

Use this when working on the TrendBoda Next.js dashboard, frontend tooling, styling, components, icons, fonts, or dashboard tests.

## Project Boundary

- Web project root is `web/`.
- Next.js app source lives under `web/app/`.
- Keep the dashboard local-first for the first slice.
- Do not add new backend APIs from web-only work.

## Before Changing Web Code

- Read root `DESIGN.md` before changing dashboard UI, styling, components, icons, or fonts.
- If `DESIGN.md` does not exist yet, check `.scratch/first-slice/issues/09-create-dashboard-design-system-contract.md` before making visual-system decisions.
- Follow `DESIGN.md` for visual-system choices and this file for implementation workflow.

## Package Manager

- Use pnpm only for web package management.
- Do not create or update `web/package-lock.json`.
- Keep `web/pnpm-lock.yaml` as the only web lockfile.
- Run web commands from the repo root with `pnpm --dir web`.

## Styling

- Use Tailwind CSS for dashboard styling.
- Keep `web/app/globals.css` limited to Tailwind imports and minimal global styles.
- Avoid broad hand-written component CSS unless Tailwind cannot express the needed behavior cleanly.
- Preserve the current dashboard behavior when migrating styles.

## Components

- Use shadcn/ui for shared UI primitives when the dashboard needs reusable buttons, cards, inputs, tabs, dialogs, tables, menus, or form controls.
- Do not introduce broad component folders or abstractions before repeated UI patterns exist.
- Existing component file names may remain kebab-case, such as `geeknews-list.tsx`.
- Exported React components must use PascalCase, such as `GeekNewsList`.
- Revisit component directory and file naming conventions later when the dashboard has enough repeated components to justify the refactor.

## Icons

- Use `lucide-react` for icons.
- Prefer lucide icons inside icon buttons and compact controls instead of custom SVGs.
- Add accessible labels or surrounding text where an icon is not self-explanatory.

## Fonts

- Use Pretendard as the primary UI font because TrendBoda's dashboard must support Korean text well.
- Keep Pretendard font files under `web/app/fonts/` instead of depending on CDN or external font delivery.
- Use `next/font/local` when bundling the local Pretendard font file.
- Keep fallback fonts as system sans-serif fonts.

## UI Tone

- TrendBoda is an operational dashboard, not a marketing site.
- Prefer dense, scannable, quiet layouts for repeated review.
- Avoid decorative hero sections, unnecessary cards inside cards, and visual effects that do not improve dashboard use.

## Commands

Use these commands after the pnpm/Tailwind migration is complete:

```bash
pnpm --dir web install
pnpm --dir web run dev
pnpm --dir web run lint
pnpm --dir web run build
```
