#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"
WEB_BASE_URL="${WEB_BASE_URL:-http://127.0.0.1:3000}"
MODE="live"

usage() {
  cat <<'USAGE'
Usage: scripts/first-slice-smoke.sh [--mocked] [--help]

First-slice smoke workflow:
  1. DB startup: docker compose up -d postgres
  2. migrations: dbmate --env-file .env --migrations-dir db/migrations up
  3. API startup: uv --directory backend run fastapi dev src/trendboda/app.py
  4. web startup: pnpm --dir web dev
  5. API health: GET /health
  6. GeekNews fetch: POST /geeknews/fetch-runs
  7. AI usage inspection: GET /ai/cost/summary and /ai/cost/requests
  8. AI Cost Dashboard: open http://127.0.0.1:3000
  9. Telegram /geeknews and /cost: run bot polling or unit-format checks

Live mode requires DATABASE_URL in .env.
Mocked mode (--mocked) skips live GeekNews fetch and Telegram secrets.

Environment:
  API_BASE_URL defaults to http://127.0.0.1:8000
  WEB_BASE_URL defaults to http://127.0.0.1:3000
USAGE
}

fail() {
  printf 'SMOKE FAIL: %s\n' "$1" >&2
  exit 1
}

pass() {
  printf 'ok: %s\n' "$1"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      usage
      exit 0
      ;;
    --mocked)
      MODE="mocked"
      shift
      ;;
    *)
      fail "unknown option: $1"
      ;;
  esac
done

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "$1 is required"
}

require_env_file() {
  [[ -f "$REPO_ROOT/.env" ]] || fail ".env is missing; copy .env.example to .env"
}

require_env_value() {
  local name="$1"
  local value
  value="$(grep -E "^${name}=" "$REPO_ROOT/.env" | tail -n 1 | cut -d= -f2- || true)"
  [[ -n "$value" ]] || fail "$name is required in .env"
}

http_json() {
  local method="$1"
  local url="$2"
  local output="$3"
  local status
  status="$(curl -sS -X "$method" -H "accept: application/json" -o "$output" -w "%{http_code}" "$url" || true)"
  [[ "$status" =~ ^2 ]] || fail "$method $url returned HTTP $status"
}

json_read() {
  local file="$1"
  local expr="$2"
  python3 - "$file" "$expr" <<'PY'
import json
import sys

path, expr = sys.argv[1], sys.argv[2]
with open(path, encoding="utf-8") as handle:
    value = json.load(handle)
for part in expr.split("."):
    if isinstance(value, list):
        value = value[int(part)]
    else:
        value = value[part]
print(value)
PY
}

cd "$REPO_ROOT"

require_command curl
require_command docker
require_command dbmate
require_command uv
require_command pnpm
require_command python3
require_env_file
require_env_value DATABASE_URL

docker compose ps postgres --status running | grep -q postgres \
  || fail "local Postgres is not running; run: docker compose up -d postgres"
pass "local Postgres running"

dbmate --env-file .env --migrations-dir db/migrations status | grep -q "Pending: 0" \
  || fail "migrations are pending or dbmate cannot reach Postgres; run: dbmate --env-file .env --migrations-dir db/migrations up"
pass "migrations current"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

http_json GET "$API_BASE_URL/health" "$tmp_dir/health.json"
[[ "$(json_read "$tmp_dir/health.json" "status")" == "ok" ]] || fail "API health did not return status=ok"
pass "API health"

if [[ "$MODE" == "live" ]]; then
  http_json POST "$API_BASE_URL/geeknews/fetch-runs" "$tmp_dir/fetch.json"
  pass "GeekNews fetch"
else
  printf 'skip: GeekNews fetch in mocked mode\n'
fi

http_json GET "$API_BASE_URL/geeknews/items" "$tmp_dir/items.json"
item_id="$(json_read "$tmp_dir/items.json" "items.0.id" 2>/dev/null || true)"
[[ -n "$item_id" ]] || fail "no GeekNews items available; run live fetch or seed local DB"
pass "GeekNews item availability"

http_json GET "$API_BASE_URL/ai/cost/summary" "$tmp_dir/cost-summary.json"
http_json GET "$API_BASE_URL/ai/cost/requests?limit=1" "$tmp_dir/cost-requests.json"
pass "AI usage inspection endpoints"

web_status="$(curl -sS -o "$tmp_dir/web.html" -w "%{http_code}" "$WEB_BASE_URL" || true)"
[[ "$web_status" =~ ^2 ]] || fail "web dashboard unavailable at $WEB_BASE_URL; run: pnpm --dir web dev"
pass "AI Cost Dashboard connectivity"

uv --directory backend run python - <<'PY'
from trendboda.telegram_bot import format_cost_message, format_geeknews_message, GeekNewsTelegramItem

geeknews = format_geeknews_message([
    GeekNewsTelegramItem(title="Smoke signal", source_url="https://example.com", content_text="Short signal")
])
cost = format_cost_message(
    {
        "totals": {"estimated_cost_usd": "0.0001", "request_count": 1, "failure_count": 0},
        "budget": {
            "estimated_monthly_cost_usd": "0.0001",
            "monthly_budget_usd": "10.00",
            "percent_used": "0.001",
        },
    },
    monthly_budget_usd="10.00",
)
assert "Smoke signal" in geeknews
assert "OpenRouter cost" in cost
PY
pass "Telegram /geeknews and /cost formatting"

printf 'first-slice smoke passed (%s)\n' "$MODE"
