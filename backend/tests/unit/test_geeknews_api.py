from datetime import UTC, datetime

from fastapi.testclient import TestClient

from trendboda.api.dependencies import get_geeknews_provider, get_repositories
from trendboda.app import app
from trendboda.geeknews import GeekNewsItem, StoredGeekNewsItem


class FakeGeekNewsRepository:
    def __init__(self) -> None:
        self.items = [
            StoredGeekNewsItem(
                id=1,
                fetch_run_id=10,
                external_id="item-1",
                title="Stored signal",
                source_url="https://news.example.com/1",
                published_at=datetime(2026, 5, 9, 10, 0, tzinfo=UTC),
                fetched_at=datetime(2026, 5, 9, 10, 5, tzinfo=UTC),
            )
        ]
        self.fetch_runs: list[dict[str, object]] = []

    async def list_recent_items(self, *, limit: int) -> list[StoredGeekNewsItem]:
        return self.items[:limit]

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
                published_at=None,
            )
        ]


class FailingProvider:
    async def fetch_items(self) -> list[GeekNewsItem]:
        raise RuntimeError("upstream unavailable")


def test_list_geeknews_items_returns_recent_items() -> None:
    app.dependency_overrides[get_repositories] = FakeRepositories
    try:
        client = TestClient(app)
        response = client.get("/geeknews/items")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["items"][0]["title"] == "Stored signal"
    assert response.json()["items"][0]["published_at"] == "2026-05-09T10:00:00+00:00"
    assert response.json()["items"][0]["fetched_at"] == "2026-05-09T10:05:00+00:00"


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
