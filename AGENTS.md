# Agent Instructions

## Agent skills

### Issue tracker

Issues and PRDs live as local markdown files under `.scratch/`; Git is for version control, not issue tracking. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-role triage vocabulary is used unchanged. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context repo: domain language lives in `CONTEXT.md`, ADRs in `docs/adr/`, plans in `docs/plan/`. See `docs/agents/domain.md`.
When PRDs or plans change how agents should work, update the relevant `docs/plan/` and `docs/agents/*` files as well as the local issue tracker.

### Backend setup

Backend Python setup, uv commands, tests, migrations, and local tooling conventions live in `docs/agents/backend.md`.

### Web setup

Next.js dashboard setup, pnpm commands, Tailwind styling, shadcn/ui, lucide icons, fonts, and component conventions live in `docs/agents/web.md`.
