from typing import Any

from trendboda.geeknews import GEEKNEWS_SOURCE_NAME, GeekNewsItem, StoredGeekNewsItem
from trendboda.repositories.types import GeekNewsSummary


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
                          content_raw_html,
                          content_text,
                          published_at
                        )
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                        ON CONFLICT (source_name, external_id) DO UPDATE
                        SET fetch_run_id = EXCLUDED.fetch_run_id,
                            title = EXCLUDED.title,
                            source_url = EXCLUDED.source_url,
                            content_raw_html = EXCLUDED.content_raw_html,
                            content_text = EXCLUDED.content_text,
                            published_at = EXCLUDED.published_at,
                            updated_at = now()
                        WHERE FALSE
                        """,
                        fetch_run_id,
                        GEEKNEWS_SOURCE_NAME,
                        item.external_id,
                        item.title,
                        item.source_url,
                        item.content_raw_html,
                        item.content_text,
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
                   content_text,
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
        return [_stored_geeknews_item(row) for row in rows]

    async def get_item(self, *, item_id: int) -> StoredGeekNewsItem | None:
        row = await self._pool.fetchrow(
            """
            SELECT id,
                   fetch_run_id,
                   external_id,
                   title,
                   source_url,
                   content_text,
                   published_at,
                   fetched_at
            FROM geeknews_items
            WHERE source_name = $1
              AND id = $2
            """,
            GEEKNEWS_SOURCE_NAME,
            item_id,
        )
        if row is None:
            return None
        return _stored_geeknews_item(row)

    async def get_summary(self, *, item_id: int) -> GeekNewsSummary | None:
        row = await self._pool.fetchrow(
            """
            SELECT item_id,
                   summary,
                   model,
                   generated_at
            FROM geeknews_summaries
            WHERE item_id = $1
            """,
            item_id,
        )
        if row is None:
            return None
        return _geeknews_summary(row)

    async def upsert_summary(
        self,
        *,
        item_id: int,
        summary: str,
        model: str,
    ) -> GeekNewsSummary:
        row = await self._pool.fetchrow(
            """
            INSERT INTO geeknews_summaries (item_id, summary, model)
            VALUES ($1, $2, $3)
            ON CONFLICT (item_id) DO UPDATE
            SET summary = EXCLUDED.summary,
                model = EXCLUDED.model,
                generated_at = now(),
                updated_at = now()
            RETURNING item_id, summary, model, generated_at
            """,
            item_id,
            summary,
            model,
        )
        return _geeknews_summary(row)


def _stored_geeknews_item(row: Any) -> StoredGeekNewsItem:
    return StoredGeekNewsItem(
        id=int(row["id"]),
        fetch_run_id=row["fetch_run_id"],
        external_id=str(row["external_id"]),
        title=str(row["title"]),
        source_url=str(row["source_url"]),
        content_text=str(row["content_text"]),
        published_at=row["published_at"],
        fetched_at=row["fetched_at"],
    )


def _geeknews_summary(row: Any) -> GeekNewsSummary:
    return GeekNewsSummary(
        item_id=int(row["item_id"]),
        summary=str(row["summary"]),
        model=str(row["model"]),
        generated_at=row["generated_at"],
    )
