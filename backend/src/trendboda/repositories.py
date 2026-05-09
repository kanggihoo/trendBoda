from dataclasses import dataclass
from typing import Any

from trendboda.geeknews import GEEKNEWS_SOURCE_NAME, GeekNewsItem, StoredGeekNewsItem


@dataclass(frozen=True)
class Repositories:
    pool: Any

    @property
    def geeknews(self) -> "GeekNewsRepository":
        return GeekNewsRepository(self.pool)


class GeekNewsRepository:
    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def record_fetch_run(
        self,
        *,
        status: str,
        item_count: int,
        error_message: str | None = None,
    ) -> int:
        row = await self._pool.fetchrow(
            """
            INSERT INTO geeknews_fetch_runs (source_name, status, item_count, error_message)
            VALUES ($1, $2, $3, $4)
            RETURNING id
            """,
            GEEKNEWS_SOURCE_NAME,
            status,
            item_count,
            error_message,
        )
        return int(row["id"])

    async def upsert_items(self, *, fetch_run_id: int, items: list[GeekNewsItem]) -> int:
        inserted_count = 0
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                for item in items:
                    result = await connection.execute(
                        """
                        INSERT INTO geeknews_items (
                          fetch_run_id,
                          source_name,
                          external_id,
                          title,
                          source_url,
                          published_at
                        )
                        VALUES ($1, $2, $3, $4, $5, $6)
                        ON CONFLICT (source_name, external_id) DO UPDATE
                        SET fetch_run_id = EXCLUDED.fetch_run_id,
                            title = EXCLUDED.title,
                            source_url = EXCLUDED.source_url,
                            published_at = EXCLUDED.published_at,
                            updated_at = now()
                        WHERE FALSE
                        """,
                        fetch_run_id,
                        GEEKNEWS_SOURCE_NAME,
                        item.external_id,
                        item.title,
                        item.source_url,
                        item.published_at,
                    )
                    if result == "INSERT 0 1":
                        inserted_count += 1
        return inserted_count

    async def list_recent_items(self, *, limit: int) -> list[StoredGeekNewsItem]:
        rows = await self._pool.fetch(
            """
            SELECT id,
                   fetch_run_id,
                   external_id,
                   title,
                   source_url,
                   published_at,
                   fetched_at
            FROM geeknews_items
            WHERE source_name = $1
            ORDER BY published_at DESC NULLS LAST, id DESC
            LIMIT $2
            """,
            GEEKNEWS_SOURCE_NAME,
            limit,
        )
        return [
            StoredGeekNewsItem(
                id=int(row["id"]),
                fetch_run_id=row["fetch_run_id"],
                external_id=str(row["external_id"]),
                title=str(row["title"]),
                source_url=str(row["source_url"]),
                published_at=row["published_at"],
                fetched_at=row["fetched_at"],
            )
            for row in rows
        ]
