import json
from decimal import Decimal, InvalidOperation
from typing import Any

from trendboda.ai import AIFeature, AIUsageStatus


class AIUsageRepository:
    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def record_ai_usage(
        self,
        *,
        feature: AIFeature | str,
        status: AIUsageStatus | str,
        requested_models: list[str],
        actual_model: str | None,
        prompt_tokens: int | None,
        completion_tokens: int | None,
        total_tokens: int | None,
        estimated_cost_usd: Decimal | None,
        latency_ms: int,
        pricing_source: str | None,
        pricing_snapshot: dict[str, Any] | None,
        error_message: str | None,
    ) -> int:
        row = await self._pool.fetchrow(
            """
            INSERT INTO ai_usage_records (
              feature,
              status,
              requested_models,
              actual_model,
              prompt_tokens,
              completion_tokens,
              total_tokens,
              estimated_cost_usd,
              latency_ms,
              pricing_source,
              pricing_snapshot,
              error_message
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11::jsonb, $12)
            RETURNING id
            """,
            str(feature),
            str(status),
            requested_models,
            actual_model,
            prompt_tokens,
            completion_tokens,
            total_tokens,
            estimated_cost_usd,
            latency_ms,
            pricing_source,
            json.dumps(pricing_snapshot) if pricing_snapshot is not None else None,
            error_message,
        )
        return int(row["id"])

    async def summarize_ai_cost(self, *, monthly_budget_usd: str = "10.00") -> dict[str, object]:
        totals = await self._pool.fetchrow(
            """
            SELECT COALESCE(SUM(estimated_cost_usd), 0)::text AS estimated_cost_usd,
                   COUNT(*)::int AS request_count,
                   COUNT(*) FILTER (WHERE status = 'success')::int AS success_count,
                   COUNT(*) FILTER (WHERE status = 'failure')::int AS failure_count,
                   ROUND(AVG(latency_ms))::int AS average_latency_ms,
                   COALESCE(SUM(estimated_cost_usd) FILTER (
                     WHERE created_at >= date_trunc('month', now())
                   ), 0)::text AS month_estimated_cost_usd
            FROM ai_usage_records
            """
        )
        by_date = await self._pool.fetch(
            """
            SELECT date_trunc('day', created_at)::date AS date,
                   COALESCE(SUM(estimated_cost_usd), 0)::text AS estimated_cost_usd,
                   COUNT(*)::int AS request_count,
                   ROUND(AVG(latency_ms))::int AS average_latency_ms,
                   COUNT(*) FILTER (WHERE status = 'failure')::int AS failure_count
            FROM ai_usage_records
            GROUP BY date
            ORDER BY date DESC
            LIMIT 31
            """
        )
        by_model = await self._pool.fetch(
            """
            SELECT COALESCE(actual_model, 'unknown') AS model,
                   COALESCE(SUM(estimated_cost_usd), 0)::text AS estimated_cost_usd,
                   COUNT(*)::int AS request_count,
                   ROUND(AVG(latency_ms))::int AS average_latency_ms,
                   COUNT(*) FILTER (WHERE status = 'failure')::int AS failure_count
            FROM ai_usage_records
            GROUP BY COALESCE(actual_model, 'unknown')
            ORDER BY SUM(estimated_cost_usd) DESC NULLS LAST, request_count DESC
            LIMIT 20
            """
        )
        by_feature = await self._pool.fetch(
            """
            SELECT feature,
                   COALESCE(SUM(estimated_cost_usd), 0)::text AS estimated_cost_usd,
                   COUNT(*)::int AS request_count,
                   ROUND(AVG(latency_ms))::int AS average_latency_ms,
                   COUNT(*) FILTER (WHERE status = 'failure')::int AS failure_count
            FROM ai_usage_records
            GROUP BY feature
            ORDER BY SUM(estimated_cost_usd) DESC NULLS LAST, request_count DESC
            LIMIT 20
            """
        )
        monthly_cost = _decimal_from_row(totals, "month_estimated_cost_usd")
        monthly_budget = _decimal(monthly_budget_usd)
        percent_used = Decimal("0")
        if monthly_budget > 0:
            percent_used = (monthly_cost / monthly_budget) * Decimal("100")
        return {
            "totals": {
                "estimated_cost_usd": _decimal_text(totals["estimated_cost_usd"]),
                "request_count": int(totals["request_count"]),
                "success_count": int(totals["success_count"]),
                "failure_count": int(totals["failure_count"]),
                "average_latency_ms": _optional_int(totals["average_latency_ms"]),
            },
            "by_date": [
                {
                    "date": _date_text(row["date"]),
                    "estimated_cost_usd": _decimal_text(row["estimated_cost_usd"]),
                    "request_count": int(row["request_count"]),
                    "average_latency_ms": _optional_int(row["average_latency_ms"]),
                    "failure_count": int(row["failure_count"]),
                }
                for row in by_date
            ],
            "by_model": [
                {
                    "model": str(row["model"]),
                    "estimated_cost_usd": _decimal_text(row["estimated_cost_usd"]),
                    "request_count": int(row["request_count"]),
                    "average_latency_ms": _optional_int(row["average_latency_ms"]),
                    "failure_count": int(row["failure_count"]),
                }
                for row in by_model
            ],
            "by_feature": [
                {
                    "feature": str(row["feature"]),
                    "estimated_cost_usd": _decimal_text(row["estimated_cost_usd"]),
                    "request_count": int(row["request_count"]),
                    "average_latency_ms": _optional_int(row["average_latency_ms"]),
                    "failure_count": int(row["failure_count"]),
                }
                for row in by_feature
            ],
            "budget": {
                "monthly_budget_usd": _decimal_text(monthly_budget),
                "estimated_monthly_cost_usd": _decimal_text(monthly_cost),
                "percent_used": _decimal_text(percent_used),
            },
        }

    async def list_ai_usage_records(self, *, limit: int) -> list[dict[str, object]]:
        rows = await self._pool.fetch(
            """
            SELECT id,
                   feature,
                   status,
                   requested_models,
                   actual_model,
                   prompt_tokens,
                   completion_tokens,
                   total_tokens,
                   COALESCE(estimated_cost_usd, 0)::text AS estimated_cost_usd,
                   latency_ms,
                   pricing_source,
                   error_message,
                   created_at
            FROM ai_usage_records
            ORDER BY created_at DESC, id DESC
            LIMIT $1
            """,
            limit,
        )
        return [
            {
                "id": int(row["id"]),
                "feature": str(row["feature"]),
                "status": str(row["status"]),
                "requested_models": list(row["requested_models"]),
                "actual_model": row["actual_model"],
                "prompt_tokens": _optional_int(row["prompt_tokens"]),
                "completion_tokens": _optional_int(row["completion_tokens"]),
                "total_tokens": _optional_int(row["total_tokens"]),
                "estimated_cost_usd": _decimal_text(row["estimated_cost_usd"]),
                "latency_ms": int(row["latency_ms"]),
                "pricing_source": row["pricing_source"],
                "error_message": row["error_message"],
                "created_at": _datetime_text(row["created_at"]),
            }
            for row in rows
        ]


def _decimal(value: object) -> Decimal:
    try:
        return Decimal(str(value))
    except InvalidOperation:
        return Decimal("0")


def _decimal_from_row(row: dict[str, object], key: str) -> Decimal:
    return _decimal(row[key])


def _decimal_text(value: object) -> str:
    decimal = _decimal(value)
    if decimal == 0:
        return "0"
    return format(decimal.normalize(), "f")


def _optional_int(value: Any) -> int | None:
    return None if value is None else int(value)


def _date_text(value: Any) -> str:
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _datetime_text(value: Any) -> str:
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)
