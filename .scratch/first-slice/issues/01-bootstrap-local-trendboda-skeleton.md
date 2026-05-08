Status: ready-for-agent
Type: AFK

# Bootstrap local TrendBoda skeleton

## Parent

.scratch/first-slice/PRD.md

## What to build

Create the local development skeleton for the TrendBoda first slice. The Owner should be able to start local Postgres, apply dbmate migrations, run FastAPI on the host through uv with a health check, run the Next.js dashboard on the host, and execute baseline tests. This slice establishes the project structure and development workflow that later GeekNews, OpenRouter, dashboard, and Telegram slices will build on.

## User stories covered

- 25. FastAPI health checks
- 35. Dockerized local Postgres
- 36. uv-managed host-run FastAPI and host-run Next.js
- 37. dbmate-managed schema changes
- 38. Repository classes as the Python-to-database boundary

## Acceptance criteria

- [ ] Local Postgres can be started through Docker Compose.
- [ ] dbmate is configured and can apply at least one initial migration.
- [ ] FastAPI starts locally and exposes a health endpoint.
- [ ] Backend Python dependencies and commands are managed through uv.
- [ ] Next.js starts locally and renders a basic TrendBoda dashboard shell.
- [ ] Backend test command exists and passes for health/config baseline tests.
- [ ] Frontend test or lint command exists and passes for the dashboard shell.
- [ ] Repository pattern and asyncpg connection-pool setup are established without SQLAlchemy.
- [ ] Local setup instructions document how to start DB, apply migrations, run API, run web, and run tests.

## Blocked by

None - can start immediately
