import pytest

from trendboda.exceptions import GeekNewsFetchFailed
from trendboda.geeknews import GeekNewsItem
from trendboda.services.geeknews import GeekNewsFetchService


class FakeGeekNewsRepository:
    def __init__(self) -> None:
        self.fetch_runs: list[dict[str, object]] = []
        self.upserted_items: list[GeekNewsItem] = []

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
        self.upserted_items = items
        return len(items)


class FakeProvider:
    async def fetch_items(self) -> list[GeekNewsItem]:
        return [
            GeekNewsItem(
                external_id="item-1",
                title="Fetched signal",
                source_url="https://news.example.com/1",
                published_at=None,
            )
        ]


class FailingProvider:
    async def fetch_items(self) -> list[GeekNewsItem]:
        raise RuntimeError("upstream unavailable")


async def test_geeknews_fetch_service_records_successful_fetch() -> None:
    repository = FakeGeekNewsRepository()
    service = GeekNewsFetchService(repository=repository, provider=FakeProvider())

    result = await service.fetch()

    assert result.fetch_run_id == 10
    assert result.fetched_count == 1
    assert result.inserted_count == 1
    assert repository.fetch_runs == [{"status": "success", "item_count": 1, "error_message": None}]


async def test_geeknews_fetch_service_records_failure_before_raising_app_error() -> None:
    repository = FakeGeekNewsRepository()
    service = GeekNewsFetchService(repository=repository, provider=FailingProvider())

    with pytest.raises(GeekNewsFetchFailed):
        await service.fetch()

    assert repository.fetch_runs == [
        {
            "status": "failure",
            "item_count": 0,
            "error_message": "upstream unavailable",
        }
    ]
