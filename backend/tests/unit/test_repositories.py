from typing import cast

from trendboda.repositories import Repositories


class FakePool:
    pass


def test_repositories_expose_shared_database_pool() -> None:
    pool = FakePool()

    repositories = Repositories(pool=pool)

    assert repositories.pool is pool


class FakeAIUsagePool:
    async def fetchrow(self, query: str, *args: object) -> dict[str, object]:
        if "COUNT(*)" in query:
            return {
                "estimated_cost_usd": "0.0085",
                "request_count": 3,
                "success_count": 2,
                "failure_count": 1,
                "average_latency_ms": 150,
                "month_estimated_cost_usd": "0.0060",
            }
        raise AssertionError(f"Unexpected query: {query}")

    async def fetch(self, query: str, *args: object) -> list[dict[str, object]]:
        if "date_trunc('day'" in query:
            return [
                {
                    "date": "2026-05-10",
                    "estimated_cost_usd": "0.0060",
                    "request_count": 2,
                    "average_latency_ms": 100,
                    "failure_count": 0,
                }
            ]
        if "COALESCE(actual_model" in query:
            return [
                {
                    "model": "openai/gpt-4.1-nano",
                    "estimated_cost_usd": "0.0050",
                    "request_count": 2,
                    "average_latency_ms": 120,
                    "failure_count": 1,
                }
            ]
        if "GROUP BY feature" in query:
            return [
                {
                    "feature": "geeknews_summary",
                    "estimated_cost_usd": "0.0085",
                    "request_count": 3,
                    "average_latency_ms": 150,
                    "failure_count": 1,
                }
            ]
        if "ORDER BY created_at DESC" in query:
            return [
                {
                    "id": 101,
                    "feature": "geeknews_summary",
                    "status": "failure",
                    "requested_models": ["openai/gpt-4.1-nano"],
                    "actual_model": None,
                    "prompt_tokens": None,
                    "completion_tokens": None,
                    "total_tokens": None,
                    "estimated_cost_usd": "0",
                    "latency_ms": 320,
                    "pricing_source": None,
                    "error_message": "rate limited",
                    "created_at": "2026-05-10T09:00:00+00:00",
                }
            ]
        raise AssertionError(f"Unexpected query: {query}")


async def test_ai_usage_repository_summarizes_cost_groupings_and_budget() -> None:
    repositories = Repositories(pool=FakeAIUsagePool())

    summary = await repositories.ai_usage.summarize_ai_cost(monthly_budget_usd="10.00")

    assert summary["totals"] == {
        "estimated_cost_usd": "0.0085",
        "request_count": 3,
        "success_count": 2,
        "failure_count": 1,
        "average_latency_ms": 150,
    }
    assert summary["by_date"] == [
        {
            "date": "2026-05-10",
            "estimated_cost_usd": "0.006",
            "request_count": 2,
            "average_latency_ms": 100,
            "failure_count": 0,
        }
    ]
    by_model = cast(list[dict[str, object]], summary["by_model"])
    by_feature = cast(list[dict[str, object]], summary["by_feature"])
    assert by_model[0]["model"] == "openai/gpt-4.1-nano"
    assert by_feature[0]["feature"] == "geeknews_summary"
    assert summary["budget"] == {
        "monthly_budget_usd": "10",
        "estimated_monthly_cost_usd": "0.006",
        "percent_used": "0.06",
    }


async def test_ai_usage_repository_lists_recent_request_detail() -> None:
    repositories = Repositories(pool=FakeAIUsagePool())

    records = await repositories.ai_usage.list_ai_usage_records(limit=1)

    assert records == [
        {
            "id": 101,
            "feature": "geeknews_summary",
            "status": "failure",
            "requested_models": ["openai/gpt-4.1-nano"],
            "actual_model": None,
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None,
            "estimated_cost_usd": "0",
            "latency_ms": 320,
            "pricing_source": None,
            "error_message": "rate limited",
            "created_at": "2026-05-10T09:00:00+00:00",
        }
    ]
