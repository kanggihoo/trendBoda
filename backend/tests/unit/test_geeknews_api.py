from datetime import UTC, datetime
from decimal import Decimal
from typing import cast

from fastapi.testclient import TestClient
from trendboda.ai import AIUsageStatus
from trendboda.api.dependencies import get_geeknews_provider, get_repositories
from trendboda.app import app
from trendboda.geeknews import GeekNewsItem, StoredGeekNewsItem
from trendboda.repositories import GeekNewsSummary


class FakeGeekNewsRepository:
    def __init__(self) -> None:
        self.items = [
            StoredGeekNewsItem(
                id=1,
                fetch_run_id=10,
                external_id="item-1",
                title="Stored signal",
                source_url="https://news.example.com/1",
                content_text="• Stored item body",
                published_at=datetime(2026, 5, 9, 10, 0, tzinfo=UTC),
                fetched_at=datetime(2026, 5, 9, 10, 5, tzinfo=UTC),
            )
        ]
        self.fetch_runs: list[dict[str, object]] = []
        self.summaries: dict[int, GeekNewsSummary] = {
            1: GeekNewsSummary(
                item_id=1,
                summary="Existing stored summary",
                model="openai/gpt-4.1-nano",
                generated_at=datetime(2026, 5, 9, 10, 6, tzinfo=UTC),
            )
        }
        self.ai_usage_records: list[dict[str, object]] = []

    async def list_recent_items(self, *, limit: int) -> list[StoredGeekNewsItem]:
        return self.items[:limit]

    async def get_item(self, *, item_id: int) -> StoredGeekNewsItem | None:
        return next((item for item in self.items if item.id == item_id), None)

    async def get_summary(self, *, item_id: int) -> GeekNewsSummary | None:
        return self.summaries.get(item_id)

    async def record_fetch_run(
        self,
        *,
        status: str,
        item_count: int,
        error_message: str | None = None,
    ) -> int:
        self.fetch_runs.append(
            {"status": status, "item_count": item_count, "error_message": error_message}
        )
        return 10

    async def upsert_items(self, *, fetch_run_id: int, items: list[GeekNewsItem]) -> int:
        return len(items)

    async def upsert_summary(
        self,
        *,
        item_id: int,
        summary: str,
        model: str,
    ) -> GeekNewsSummary:
        stored = GeekNewsSummary(
            item_id=item_id,
            summary=summary,
            model=model,
            generated_at=datetime(2026, 5, 9, 10, 7, tzinfo=UTC),
        )
        self.summaries[item_id] = stored
        return stored

    async def record_ai_usage(self, **record: object) -> int:
        self.ai_usage_records.append(record)
        return len(self.ai_usage_records)


class FakeRepositories:
    def __init__(self) -> None:
        self.geeknews = FakeGeekNewsRepository()


class FakeProvider:
    async def fetch_items(self) -> list[GeekNewsItem]:
        return [
            GeekNewsItem(
                external_id="new-1",
                title="New signal",
                source_url="https://news.example.com/new",
                content_raw_html="<ul><li>New item body</li></ul>",
                content_text="• New item body",
                published_at=None,
            )
        ]


class FailingProvider:
    async def fetch_items(self) -> list[GeekNewsItem]:
        raise RuntimeError("upstream unavailable")


class FakeSummaryGateway:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    async def complete(self, *, models: list[str], messages: list[dict[str, str]]):
        from trendboda.ai import OpenRouterResult

        self.calls.append({"models": models, "messages": messages})
        return OpenRouterResult(
            status=AIUsageStatus.SUCCESS,
            content="Generated owner-ready summary",
            actual_model="google/gemini-2.5-flash-lite",
            prompt_tokens=12,
            completion_tokens=6,
            total_tokens=18,
            latency_ms=25,
        )


class FailingSummaryGateway:
    async def complete(self, *, models: list[str], messages: list[dict[str, str]]):
        from trendboda.ai import OpenRouterResult

        return OpenRouterResult(
            status=AIUsageStatus.FAILURE,
            content=None,
            actual_model="openai/gpt-4.1-nano",
            prompt_tokens=None,
            completion_tokens=None,
            total_tokens=None,
            latency_ms=30,
            error_message="rate limited",
        )


class FakePricingCatalog:
    async def get_pricing(self, model: str):
        from decimal import Decimal

        from trendboda.ai import OpenRouterModelPricing

        return OpenRouterModelPricing(
            prompt_per_million=Decimal("0.10"),
            completion_per_million=Decimal("0.40"),
            source="test",
            raw={"prompt": "0.10", "completion": "0.40"},
        )


def test_list_geeknews_items_returns_recent_items() -> None:
    app.dependency_overrides[get_repositories] = FakeRepositories
    try:
        client = TestClient(app)
        response = client.get("/geeknews/items")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["items"][0]["title"] == "Stored signal"
    assert response.json()["items"][0]["content_text"] == "• Stored item body"
    assert response.json()["items"][0]["published_at"] == "2026-05-09T10:00:00+00:00"
    assert response.json()["items"][0]["fetched_at"] == "2026-05-09T10:05:00+00:00"
    assert response.json()["items"][0]["summary"]["summary"] == "Existing stored summary"


def test_list_geeknews_items_returns_empty_list() -> None:
    repositories = FakeRepositories()
    repositories.geeknews.items = []
    app.dependency_overrides[get_repositories] = lambda: repositories
    try:
        client = TestClient(app)
        response = client.get("/geeknews/items")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"items": []}


def test_fetch_geeknews_records_run_and_insert_count() -> None:
    repositories = FakeRepositories()
    app.dependency_overrides[get_repositories] = lambda: repositories
    app.dependency_overrides[get_geeknews_provider] = FakeProvider
    try:
        client = TestClient(app)
        response = client.post("/geeknews/fetch")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"fetch_run_id": 10, "fetched_count": 1, "inserted_count": 1}
    assert repositories.geeknews.fetch_runs == [
        {"status": "success", "item_count": 1, "error_message": None}
    ]


def test_fetch_geeknews_records_failure_run() -> None:
    repositories = FakeRepositories()
    app.dependency_overrides[get_repositories] = lambda: repositories
    app.dependency_overrides[get_geeknews_provider] = FailingProvider
    try:
        client = TestClient(app)
        response = client.post("/geeknews/fetch")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 502
    assert response.json() == {
        "error": {
            "code": "geeknews_fetch_failed",
            "message": "GeekNews fetch failed",
            "request_id": response.headers["x-request-id"],
        }
    }
    assert repositories.geeknews.fetch_runs == [
        {
            "status": "failure",
            "item_count": 0,
            "error_message": "upstream unavailable",
        }
    ]


def test_get_geeknews_summary_returns_stored_summary() -> None:
    app.dependency_overrides[get_repositories] = FakeRepositories
    try:
        client = TestClient(app)
        response = client.get("/geeknews/items/1/summary")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "item_id": 1,
        "summary": "Existing stored summary",
        "model": "openai/gpt-4.1-nano",
        "generated_at": "2026-05-09T10:06:00+00:00",
    }


def test_generate_geeknews_summary_stores_summary_and_usage() -> None:
    from trendboda.api.dependencies import get_openrouter_gateway, get_pricing_catalog

    repositories = FakeRepositories()
    gateway = FakeSummaryGateway()
    app.dependency_overrides[get_repositories] = lambda: repositories
    app.dependency_overrides[get_openrouter_gateway] = lambda: gateway
    app.dependency_overrides[get_pricing_catalog] = FakePricingCatalog
    try:
        client = TestClient(app)
        response = client.post("/geeknews/items/1/summary")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["summary"] == "Generated owner-ready summary"
    assert response.json()["model"] == "google/gemini-2.5-flash-lite"
    messages = cast(list[dict[str, str]], gateway.calls[0]["messages"])
    assert messages[1]["content"] == (
        "Title: Stored signal\nURL: https://news.example.com/1\nContent: • Stored item body"
    )
    assert repositories.geeknews.ai_usage_records == [
        {
            "feature": "geeknews_summary",
            "status": "success",
            "requested_models": ["openai/gpt-4.1-nano", "google/gemini-2.5-flash-lite"],
            "actual_model": "google/gemini-2.5-flash-lite",
            "prompt_tokens": 12,
            "completion_tokens": 6,
            "total_tokens": 18,
            "estimated_cost_usd": Decimal("0.0000036"),
            "latency_ms": 25,
            "pricing_source": "test",
            "pricing_snapshot": {"prompt": "0.10", "completion": "0.40"},
            "error_message": None,
        }
    ]


def test_generate_geeknews_summary_records_failed_usage() -> None:
    from trendboda.api.dependencies import get_openrouter_gateway, get_pricing_catalog

    repositories = FakeRepositories()
    repositories.geeknews.summaries = {}
    app.dependency_overrides[get_repositories] = lambda: repositories
    app.dependency_overrides[get_openrouter_gateway] = FailingSummaryGateway
    app.dependency_overrides[get_pricing_catalog] = FakePricingCatalog
    try:
        client = TestClient(app)
        response = client.post("/geeknews/items/1/summary")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 502
    assert response.json()["error"]["code"] == "geeknews_summary_failed"
    assert repositories.geeknews.summaries == {}
    assert repositories.geeknews.ai_usage_records[0]["status"] == "failure"
    assert repositories.geeknews.ai_usage_records[0]["error_message"] == "rate limited"
