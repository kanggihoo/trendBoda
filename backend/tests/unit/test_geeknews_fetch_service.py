import pytest
from trendboda.exceptions import GeekNewsFetchFailed
from trendboda.geeknews import GeekNewsItem, StoredGeekNewsItem
from trendboda.services.geeknews import GeekNewsFetchService
from trendboda.repositories.types import GeekNewsInsertResult
from datetime import datetime, UTC


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

    async def insert_new_items(self, *, fetch_run_id: int, items: list[GeekNewsItem]) -> GeekNewsInsertResult:
        self.upserted_items = items
        stored_items = [
            StoredGeekNewsItem(
                id=idx,
                fetch_run_id=fetch_run_id,
                external_id=item.external_id,
                title=item.title,
                source_url=item.source_url,
                content_text=item.content_text,
                published_at=item.published_at,
                fetched_at=datetime.now(UTC),
            )
            for idx, item in enumerate(items, 1)
        ]
        return GeekNewsInsertResult(inserted_count=len(items), inserted_items=stored_items)


class FakeProvider:
    async def fetch_items(self) -> list[GeekNewsItem]:
        return [
            GeekNewsItem(
                external_id="item-1",
                title="Fetched signal",
                source_url="https://news.example.com/1",
                content_raw_html="<ul><li>Item body</li></ul>",
                content_text="• Item body",
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
