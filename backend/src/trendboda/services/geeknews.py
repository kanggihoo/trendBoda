from dataclasses import dataclass
from typing import Protocol

from trendboda.exceptions import GeekNewsFetchFailed
from trendboda.geeknews import GeekNewsItem


class GeekNewsRepository(Protocol):
    async def record_fetch_run(
        self,
        *,
        status: str,
        item_count: int,
        error_message: str | None = None,
    ) -> int: ...

    async def upsert_items(self, *, fetch_run_id: int, items: list[GeekNewsItem]) -> int: ...


class GeekNewsProvider(Protocol):
    async def fetch_items(self) -> list[GeekNewsItem]: ...


@dataclass(frozen=True)
class GeekNewsFetchResult:
    fetch_run_id: int
    fetched_count: int
    inserted_count: int


@dataclass(frozen=True)
class GeekNewsFetchService:
    repository: GeekNewsRepository
    provider: GeekNewsProvider

    async def fetch(self) -> GeekNewsFetchResult:
        try:
            items = await self.provider.fetch_items()
        except Exception as exc:
            await self.repository.record_fetch_run(
                status="failure",
                item_count=0,
                error_message=str(exc),
            )
            raise GeekNewsFetchFailed() from exc

        fetch_run_id = await self.repository.record_fetch_run(
            status="success",
            item_count=len(items),
        )
        inserted_count = await self.repository.upsert_items(fetch_run_id=fetch_run_id, items=items)
        return GeekNewsFetchResult(
            fetch_run_id=fetch_run_id,
            fetched_count=len(items),
            inserted_count=inserted_count,
        )
