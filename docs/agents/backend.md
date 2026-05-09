# Backend Agent Notes

Use this when working on the TrendBoda FastAPI backend, Python tests, database migrations, or local backend tooling.

## Before Changing Backend Code

- Read `CONTEXT.md` before naming TrendBoda domain concepts.
- Read `docs/adr/0003-fastapi-asyncpg-repositories-and-dbmate.md` before changing data access, repository, uv, or dbmate patterns.
- Read `docs/adr/0007-local-development-runs-apps-on-host-with-dockerized-postgres.md` before changing local process topology.
- Read `.scratch/first-slice/PRD.md` and `docs/plan/first-slice.md` before changing first-slice scope or implementation order.

## Project Boundary

- Backend Python project root is `backend/`.
- Python source lives under `backend/src/trendboda/`.
- Python tests live under `backend/tests/`.
- Database migrations live under `db/migrations/`.
- Repo root `.env` is the local configuration file. Do not move backend-only env files under `backend/`.

## Standard Commands

Run backend commands from the repo root with `uv --directory backend`.

```bash
uv --directory backend sync
uv --directory backend run pytest
uv --directory backend run pytest -m integration
uv --directory backend run ruff check .
uv --directory backend run ruff format .
uv --directory backend run ruff format --check .
uv --directory backend run pyright
```

Do not assume `cd backend` is the standard workflow. The repo root also owns `.env`, `db/`, `.vscode/`, and future web app files.

## Python Environment

- Python version is pinned to 3.12 in `backend/.python-version`.
- `backend/.venv` is managed by `uv`.
- VS Code/Antigravity should use `backend/.venv/bin/python`.
- Runtime config is loaded through `pydantic-settings` from the repo root `.env`.

## Tests

- Default `uv --directory backend run pytest` runs non-integration tests only.
- Integration tests are marked with `@pytest.mark.integration`.
- Integration tests are run explicitly with `uv --directory backend run pytest -m integration`.
- Integration tests may require Docker Desktop running, Testcontainers, Postgres, and dbmate.
- Do not make default tests depend on Docker, live network calls, OpenRouter, or Telegram.
- Keep parser, routing, cost calculation, and formatting tests as unit tests when possible.
- Use integration tests for repository behavior, dbmate migrations, and API contracts that need Postgres.

## Database Migrations

- dbmate is a host-installed CLI, not a Python dependency.
- Use dbmate SQL migrations with explicit `-- migrate:up` and `-- migrate:down` sections.
- Apply local migrations with:

```bash
dbmate --env-file .env --migrations-dir db/migrations up
```

- Check status with:

```bash
dbmate --env-file .env --migrations-dir db/migrations status
```

- Integration tests should apply migrations with `dbmate up` against a Testcontainers Postgres database rather than creating schema directly in Python.

## Static Analysis

- Ruff owns Python formatting, linting, and import sorting.
- Pyright owns type checking.
- Pyright is strict for `src` and basic for `tests`.
- Prettier owns JSON, Markdown, YAML, and future frontend files. Do not use Prettier for Python.

## Current First Slice Direction

- The first backend slice starts with GeekNews as a **Developer Trend Source**.
- Store fetch runs separately from items.
- Prevent duplicate GeekNews items with a stable external identifier.
- Repository classes are the Python-to-database boundary. Do not build ad hoc SQL in services.
- Use dbmate migrations as the source of truth for database schema.
