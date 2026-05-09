Status: ready-for-agent
Type: AFK

# Standardize web tooling with pnpm, Tailwind, and shadcn/ui

## Parent

.scratch/first-slice/PRD.md

## What to build

Move the Next.js dashboard project to a single pnpm-based package workflow and Tailwind CSS styling foundation before more dashboard features are added. The completed work should remove npm lockfile ambiguity, make web commands reproducible through pnpm, set the frontend baseline for shadcn/ui, lucide-react icons, and Pretendard typography, and migrate the current dashboard shell styling from hand-written component CSS to Tailwind utilities without changing product behavior.

This issue is a tooling and presentation foundation for the first-slice dashboard. It should not add new dashboard product features, new backend APIs, or broad component abstractions.

Keep the current web component file structure and naming during this issue. Component files such as `geeknews-list.tsx` may remain kebab-case as long as exported React components use PascalCase. Revisit component directories and naming conventions later when the dashboard has enough repeated components to justify that refactor.

## User stories covered

- 29. Show GeekNews items in the Next.js dashboard
- 30. Show OpenRouter cost metrics in the dashboard
- 36. uv-managed host-run FastAPI and host-run Next.js
- 39. Test parser, storage, API, and dashboard behavior

## Acceptance criteria

- [ ] Web package management is standardized on pnpm only.
- [ ] `web/package.json` declares the pnpm package manager version.
- [ ] `web/pnpm-lock.yaml` exists and is the only web lockfile.
- [ ] `web/package-lock.json` is removed.
- [ ] Tailwind CSS is installed and configured for the current Next.js app structure.
- [ ] shadcn/ui is initialized or documented in the web setup so future shared UI primitives follow one convention.
- [ ] `lucide-react` is available for dashboard icons.
- [ ] Pretendard font files are stored under `web/app/fonts/` and loaded through `next/font/local`.
- [ ] Pretendard is set as the primary dashboard UI font, with system sans-serif fallbacks.
- [ ] `web/app/globals.css` keeps only Tailwind imports and minimal global styles.
- [ ] Existing dashboard shell and GeekNews list visual behavior is preserved while using Tailwind utilities.
- [ ] Current component file names and structure are preserved unless a change is strictly required for Tailwind or pnpm setup.
- [ ] Existing web scripts are runnable through pnpm.
- [ ] Local setup docs and smoke workflow references use pnpm commands instead of npm commands.
- [ ] `docs/agents/web.md` remains aligned with the implemented web tooling decisions.
- [ ] No new dashboard product features are added in this issue.

## Blocked by

- .scratch/first-slice/issues/02-collect-and-display-geeknews-items.md
- .scratch/first-slice/issues/09-create-dashboard-design-system-contract.md
