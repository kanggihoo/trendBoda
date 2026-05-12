from typing import Any

from trendboda.geeknews import GEEKNEWS_SOURCE_NAME, GeekNewsItem, StoredGeekNewsItem
from trendboda.repositories.types import GeekNewsInsertResult, GeekNewsSummary


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

    async def insert_new_items(self, *, fetch_run_id: int, items: list[GeekNewsItem]) -> GeekNewsInsertResult:
        if not items:
            return GeekNewsInsertResult(inserted_count=0, inserted_items=[])

        external_ids = [item.external_id for item in items]
        titles = [item.title for item in items]
        source_urls = [item.source_url for item in items]
        content_raw_htmls = [item.content_raw_html for item in items]
        content_texts = [item.content_text for item in items]
        published_ats = [item.published_at for item in items]

        rows = await self._pool.fetch(
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
            SELECT $1, $2, external_id, title, source_url, content_raw_html, content_text, published_at
            FROM UNNEST(
                $3::text[],
                $4::text[],
                $5::text[],
                $6::text[],
                $7::text[],
                $8::timestamptz[]
            ) AS t(external_id, title, source_url, content_raw_html, content_text, published_at)
            ON CONFLICT (source_name, external_id) DO NOTHING
            RETURNING id, fetch_run_id, external_id, title, source_url, content_text, published_at, fetched_at
            """,
            fetch_run_id,
            GEEKNEWS_SOURCE_NAME,
            external_ids,
            titles,
            source_urls,
            content_raw_htmls,
            content_texts,
            published_ats,
        )

        inserted_items = [_stored_geeknews_item(row) for row in rows]
        return GeekNewsInsertResult(
            inserted_count=len(inserted_items),
            inserted_items=inserted_items,
        )

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
