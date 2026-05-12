# First Slice Smoke Workflow

This workflow proves the local TrendBoda first slice as one coherent Owner loop:
Dockerized Postgres, dbmate migrations, host-run FastAPI, host-run Next.js,
GeekNews Signal collection, AI Cost Dashboard visibility,
and Interactive Bot command formatting.

## Fresh Checkout Setup

From the repo root:

```bash
cp .env.example .env
uv --directory backend sync
pnpm --dir web install
docker compose up -d postgres
dbmate --env-file .env --migrations-dir db/migrations up
```

Start the API in one terminal:

```bash
uv --directory backend run fastapi dev src/trendboda/app.py
```

Start the web dashboard in another terminal:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 pnpm --dir web dev
```

For live Telegram polling, start a third terminal after setting Telegram env:

```bash
uv --directory backend run python -m trendboda.telegram_bot
```

## Smoke Check

Run live smoke after Postgres, migrations, API, and web are running:

```bash
scripts/first-slice-smoke.sh
```

Run no-network/mocked smoke when OpenRouter or live GeekNews fetch should be skipped:

```bash
scripts/first-slice-smoke.sh --mocked
```

Mocked mode still checks local Postgres, migrations, API health, existing GeekNews
item availability, AI cost API connectivity, dashboard connectivity, and Telegram
`/geeknews` plus `/cost` formatter behavior. Seed or fetch at least one GeekNews
item before using mocked mode.

## What The Script Verifies

- Local Postgres is running through `docker compose`.
- dbmate reports `Pending: 0` for `db/migrations`.
- FastAPI `/health` returns `status=ok`.
- Live mode can call `POST /geeknews/fetch-runs`.
- `GET /geeknews/items` returns at least one item.
- Live mode does not require or expose GeekNews summary generation.
- AI usage endpoints respond through `/ai/cost/summary` and `/ai/cost/requests`.
- Web dashboard responds at `WEB_BASE_URL`, including AI Cost Dashboard API connectivity.
- Telegram `/geeknews` and `/cost` formatting remains callable without live Telegram.

## Environment Variables

Required for live smoke:

- `DATABASE_URL`: Postgres URL used by FastAPI and dbmate.
- `OPENROUTER_API_KEY`: not required for the GeekNews Signal smoke path; set it only when manually exercising future AI-backed endpoints.

Required only for live Telegram polling:

- `TELEGRAM_BOT_TOKEN`: Telegram bot token.
- `TELEGRAM_ALLOWED_CHAT_IDS`: optional allow-list. Empty means local owner-only checks are not enforced by chat id.

Useful local overrides:

- `NEXT_PUBLIC_API_BASE_URL`: web dashboard API base URL. Use `http://127.0.0.1:8000` locally.
- `API_BASE_URL`: smoke script API URL. Defaults to `http://127.0.0.1:8000`.
- `WEB_BASE_URL`: smoke script web URL. Defaults to `http://127.0.0.1:3000`.
- `GEEKNEWS_SCHEDULER_INTERVAL_SECONDS`: overrides the default 7200 (two-hour) interval for the scheduler's run-forever mode.
Can be omitted in no-network/mocked mode:

- `OPENROUTER_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ALLOWED_CHAT_IDS`

## Clear Failure Cases

- Missing `.env` fails with instruction to copy `.env.example`.
- Missing `DATABASE_URL` fails before contacting services.
- Missing `OPENROUTER_API_KEY` does not block the GeekNews Signal smoke path.
- Stopped local Postgres fails with `docker compose up -d postgres`.
- Pending migrations fail with the exact dbmate migration command.
- Stopped FastAPI fails on `/health`.
- Missing GeekNews data fails with instruction to run live fetch or seed local DB.
- Stopped web dashboard fails with the exact `pnpm --dir web dev` command.

## First-Slice Boundaries

In scope: GeekNews as Developer Trend Source producing GeekNews Signals for scanning and link navigation, OpenRouter foundation and AI cost tracking for future AI-backed features, dashboard inspection, and Interactive Bot `/geeknews` plus `/cost`.

Out of scope:

- market data
- disclosures
- GitHub trends
- EC2 deployment
- Caddy
- OpenTofu
- Grafana
- Vercel deployment
- Rust Ops CLI
- delivery tracking storage
- automatic retry queues
