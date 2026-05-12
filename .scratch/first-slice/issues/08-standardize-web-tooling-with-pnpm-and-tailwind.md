Status: done
Type: AFK

# Standardize web tooling with pnpm, Tailwind, and shadcn/ui

## Parent

.scratch/first-slice/PRD.md

## What to build

Move the Next.js dashboard project to a single pnpm-based package workflow and Tailwind CSS styling foundation before more dashboard features are added. The completed work should remove npm lockfile ambiguity, make web commands reproducible through pnpm, set the frontend baseline for shadcn/ui, lucide-react icons, and Pretendard typography, and migrate the current dashboard shell styling from hand-written component CSS to Tailwind utilities without changing product behavior.

This issue is a tooling and presentation foundation for the first-slice dashboard. It should not add new dashboard product features, new backend APIs, or broad component abstractions.

Keep the current web component file structure and naming during this issue. Component files such as `geeknews-list.tsx` may remain kebab-case as long as exported React components use PascalCase. Revisit component directories and naming conventions later when the dashboard has enough repeated components to justify that refactor.

Use the root `DESIGN-v2.md` contract as the source for Tailwind design tokens. Generate the Tailwind token file inside the web project, not at the repository root:

```bash
pnpm dlx @google/design.md export --format tailwind DESIGN-v2.md > web/tailwind.theme.json
```

`web/tailwind.theme.json` should be committed as the generated token snapshot consumed by `web/tailwind.config.*`, so Tailwind remains usable without re-running the exporter. If the exporter omits details that `DESIGN-v2.md` defines, such as typography line heights, keep those small adjustments in `web/tailwind.config.*` and document the reason there. Do not keep a root-level `tailwind.theme.json`; it is only a temporary export path during manual experimentation.

## User stories covered

- 29. Show GeekNews items in the Next.js dashboard
- 30. Show OpenRouter cost metrics in the dashboard
- 36. uv-managed host-run FastAPI and host-run Next.js
- 39. Test parser, storage, API, and dashboard behavior

## Acceptance criteria

- [x] Web package management is standardized on pnpm only.
- [x] `web/package.json` declares the pnpm package manager version.
- [x] `web/pnpm-lock.yaml` exists and is the only web lockfile.
- [x] `web/package-lock.json` is removed.
- [x] Tailwind CSS is installed and configured for the current Next.js app structure.
- [x] `web/tailwind.theme.json` is generated from `DESIGN-v2.md` and consumed by Tailwind config.
- [x] The design token export command is documented for future regeneration.
- [x] shadcn/ui is initialized or documented in the web setup so future shared UI primitives follow one convention.
- [x] `lucide-react` is available for dashboard icons.
- [x] Pretendard font files are stored under `web/app/fonts/` and loaded through `next/font/local`.
- [x] Pretendard is set as the primary dashboard UI font, with system sans-serif fallbacks.
- [x] `web/app/globals.css` keeps only Tailwind imports and minimal global styles.
- [x] Existing dashboard shell and GeekNews list visual behavior is preserved while using Tailwind utilities.
- [x] Current component file names and structure are preserved unless a change is strictly required for Tailwind or pnpm setup.
- [x] Existing web scripts are runnable through pnpm.
- [x] Local setup docs and smoke workflow references use pnpm commands instead of npm commands.
- [x] `docs/agents/web.md` remains aligned with the implemented web tooling decisions.
- [x] No new dashboard product features are added in this issue.

## Blocked by

- .scratch/first-slice/issues/02-collect-and-display-geeknews-items.md
- .scratch/first-slice/issues/09-create-dashboard-design-system-contract.md

## Comments

- Implemented pnpm-only web package management, Tailwind setup from `DESIGN-v2.md`, shadcn/ui baseline config, lucide dependency, local Pretendard font loading, Tailwind-based dashboard shell styles, pnpm docs, and web smoke guards.
- Verified with `pnpm --dir web run lint` and `pnpm --dir web run build`.
