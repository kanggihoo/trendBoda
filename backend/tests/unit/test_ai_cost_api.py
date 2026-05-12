from typing import Any

from fastapi.testclient import TestClient

from trendboda.api.dependencies import get_repositories
from trendboda.app import app


class FakeAIUsageRepository:
    async def summarize_ai_cost(self, *, monthly_budget_usd: str) -> dict[str, object]:
        return {
            "totals": {
                "estimated_cost_usd": "0",
                "request_count": 0,
                "success_count": 0,
                "failure_count": 0,
                "average_latency_ms": None,
            },
            "by_date": [],
            "by_model": [],
            "by_feature": [],
            "budget": {
                "monthly_budget_usd": monthly_budget_usd,
                "estimated_monthly_cost_usd": "0",
                "percent_used": "0",
            },
        }

    async def list_ai_usage_records(self, *, limit: int) -> list[dict[str, Any]]:
        return [
            {
                "id": 101,
                "feature": "geeknews_summary",
                "status": "failure",
                "requested_models": ["openai/gpt-4.1-nano"],
                "actual_model": "openai/gpt-4.1-nano",
                "prompt_tokens": None,
                "completion_tokens": None,
                "total_tokens": None,
                "estimated_cost_usd": "0",
                "latency_ms": 320,
                "pricing_source": None,
                "error_message": "rate limited",
                "created_at": "2026-05-10T09:00:00+00:00",
            }
        ][:limit]


class FakeRepositories:
    def __init__(self) -> None:
        self.ai_usage = FakeAIUsageRepository()


class GroupedAIUsageRepository(FakeAIUsageRepository):
    async def summarize_ai_cost(self, *, monthly_budget_usd: str) -> dict[str, object]:
        summary = await super().summarize_ai_cost(monthly_budget_usd=monthly_budget_usd)
        summary["by_date"] = [
            {
                "date": "2026-05-10",
                "estimated_cost_usd": "0.001",
                "request_count": 1,
                "average_latency_ms": 120,
                "failure_count": 0,
            }
        ]
        summary["by_model"] = [
            {
                "model": "openai/gpt-4.1-nano",
                "estimated_cost_usd": "0.001",
                "request_count": 1,
                "average_latency_ms": 120,
                "failure_count": 0,
            }
        ]
        summary["by_feature"] = [
            {
                "feature": "market_question",
                "estimated_cost_usd": "0.001",
                "request_count": 1,
                "average_latency_ms": 120,
                "failure_count": 0,
            }
        ]
        return summary


class GroupedRepositories:
    def __init__(self) -> None:
        self.ai_usage = GroupedAIUsageRepository()


def test_ai_cost_summary_returns_empty_product_dashboard_state() -> None:
    app.dependency_overrides[get_repositories] = FakeRepositories
    try:
        client = TestClient(app)
        response = client.get("/ai/cost/summary")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "totals": {
            "estimated_cost_usd": "0",
            "request_count": 0,
            "success_count": 0,
            "failure_count": 0,
            "average_latency_ms": None,
        },
        "by_date": [],
        "by_model": [],
        "by_feature": [],
        "budget": {
            "monthly_budget_usd": "10.00",
            "estimated_monthly_cost_usd": "0",
            "percent_used": "0",
        },
    }


def test_ai_cost_summary_returns_typed_group_fields() -> None:
    app.dependency_overrides[get_repositories] = GroupedRepositories
    try:
        client = TestClient(app)
        response = client.get("/ai/cost/summary")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["by_date"][0] == {
        "estimated_cost_usd": "0.001",
        "request_count": 1,
        "average_latency_ms": 120,
        "failure_count": 0,
        "date": "2026-05-10",
    }
    assert response.json()["by_model"][0] == {
        "estimated_cost_usd": "0.001",
        "request_count": 1,
        "average_latency_ms": 120,
        "failure_count": 0,
        "model": "openai/gpt-4.1-nano",
    }
    assert response.json()["by_feature"][0] == {
        "estimated_cost_usd": "0.001",
        "request_count": 1,
        "average_latency_ms": 120,
        "failure_count": 0,
        "feature": "market_question",
    }


def test_ai_cost_requests_return_recent_usage_detail() -> None:
    app.dependency_overrides[get_repositories] = FakeRepositories
    try:
        client = TestClient(app)
        response = client.get("/ai/cost/requests?limit=1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "requests": [
            {
                "id": 101,
                "feature": "geeknews_summary",
                "status": "failure",
                "requested_models": ["openai/gpt-4.1-nano"],
                "actual_model": "openai/gpt-4.1-nano",
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
    }


def test_ai_cost_requests_reject_invalid_limit() -> None:
    app.dependency_overrides[get_repositories] = FakeRepositories
    try:
        client = TestClient(app)
        response = client.get("/ai/cost/requests?limit=0")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
