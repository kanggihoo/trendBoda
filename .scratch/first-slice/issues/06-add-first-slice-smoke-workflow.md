Status: done
Type: AFK

# Add first-slice smoke workflow

## Parent

.scratch/first-slice/PRD.md

## What to build

Add an end-to-end local smoke workflow that proves the first slice works as a coherent TrendBoda loop. The Owner should be able to follow one documented path to start local services, apply migrations, fetch GeekNews, generate a summary, inspect AI cost in the dashboard, and check Telegram commands. The workflow should also keep first-slice boundaries explicit so market data, disclosures, cloud deployment, and the Rust Ops CLI remain out of scope.

## User stories covered

- 39. Test local development and end-to-end first-slice behavior
- 40. Keep market data and disclosure work excluded from this slice

## Acceptance criteria

- [x] A documented local smoke workflow covers DB startup, migrations, API startup, web startup, GeekNews fetch, summary generation, cost dashboard inspection, and Telegram command checks.
- [x] A runnable smoke test or checklist verifies API health, migration status, GeekNews item availability, AI usage recording, and dashboard API connectivity.
- [x] The workflow documents which environment variables are required and which can be omitted for no-network or mocked test mode.
- [x] The workflow explicitly lists first-slice out-of-scope areas: market data, disclosures, GitHub trends, EC2 deployment, Caddy, OpenTofu, Grafana, Vercel deployment, and Rust Ops CLI.
- [x] The smoke workflow can be run after a fresh checkout without relying on cloud deployment.
- [x] Tests or scripts fail clearly when local Postgres, migrations, API, or required secrets are missing.

## Blocked by

- .scratch/first-slice/issues/05-add-telegram-interactive-bot-commands.md
- .scratch/first-slice/issues/08-standardize-web-tooling-with-pnpm-and-tailwind.md

## Comments

- Added `docs/first-slice-smoke.md` for fresh checkout setup, live and mocked smoke paths, env vars, clear failure cases, and explicit first-slice exclusions.
- Added `scripts/first-slice-smoke.sh` to verify local Postgres, dbmate migration status, API health, GeekNews item availability, live fetch/summary where enabled, AI cost APIs, web dashboard connectivity, and Telegram formatter behavior.
- Added backend unit tests for the smoke workflow public contract.
- Verified with `uv --directory backend run pytest`.
