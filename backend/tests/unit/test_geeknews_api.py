from datetime import UTC, datetime

from fastapi.testclient import TestClient

from trendboda.app import app, get_geeknews_provider, get_repositories
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

    async def list_recent_items(self, *, limit: int) -> list[StoredGeekNewsItem]:
        return self.items[:limit]

    async def record_fetch_run(
        self,
        *,
        status: str,
        item_count: int,
        error_message: str | None = None,
    ) -> int:
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


def test_list_geeknews_items_returns_recent_items() -> None:
    app.dependency_overrides[get_repositories] = FakeRepositories
    try:
        with TestClient(app) as client:
            response = client.get("/geeknews/items")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["items"][0]["title"] == "Stored signal"


def test_fetch_geeknews_records_run_and_insert_count() -> None:
    app.dependency_overrides[get_repositories] = FakeRepositories
    app.dependency_overrides[get_geeknews_provider] = FakeProvider
    try:
        with TestClient(app) as client:
            response = client.post("/geeknews/fetch")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {"fetch_run_id": 10, "fetched_count": 1, "inserted_count": 1}
