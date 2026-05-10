import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any

from trendboda.ai import AIFeature, AIUsageStatus
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
        """RSS 수집 실행 기록 저장. 생성된 ID 반환."""
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

    # TODO : 개선 방법 (배치 처리):
    async def upsert_items(self, *, fetch_run_id: int, items: list[GeekNewsItem]) -> int:
        """뉴스 아이템 저장 또는 업데이트. 신규 삽입 개수 반환."""
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
        """최신 뉴스 아이템 목록 조회."""
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
        return [
            StoredGeekNewsItem(
                id=int(row["id"]),
                fetch_run_id=row["fetch_run_id"],
                external_id=str(row["external_id"]),
                title=str(row["title"]),
                source_url=str(row["source_url"]),
                content_text=str(row["content_text"]),
                published_at=row["published_at"],
                fetched_at=row["fetched_at"],
            )
            for row in rows
        ]

    async def get_item(self, *, item_id: int) -> StoredGeekNewsItem | None:
        """단일 뉴스 아이템 상세 조회."""
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

    async def get_summary(self, *, item_id: int) -> "GeekNewsSummary | None":
        """뉴스 아이템 AI 요약 결과 조회."""
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
        return GeekNewsSummary(
            item_id=int(row["item_id"]),
            summary=str(row["summary"]),
            model=str(row["model"]),
            generated_at=row["generated_at"],
        )

    async def upsert_summary(
        self,
        *,
        item_id: int,
        summary: str,
        model: str,
    ) -> "GeekNewsSummary":
        """AI 요약 저장 또는 업데이트."""
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
        return GeekNewsSummary(
            item_id=int(row["item_id"]),
            summary=str(row["summary"]),
            model=str(row["model"]),
            generated_at=row["generated_at"],
        )

    async def record_ai_usage(
        self,
        *,
        feature: AIFeature | str,
        status: AIUsageStatus | str,
        requested_models: list[str],
        actual_model: str | None,
        prompt_tokens: int | None,
        completion_tokens: int | None,
        total_tokens: int | None,
        estimated_cost_usd: Decimal | None,
        latency_ms: int,
        pricing_source: str | None,
        pricing_snapshot: dict[str, Any] | None,
        error_message: str | None,
    ) -> int:
        """AI 모델 사용량 및 비용 기록 저장."""
        row = await self._pool.fetchrow(
            """
            INSERT INTO ai_usage_records (
              feature,
              status,
              requested_models,
              actual_model,
              prompt_tokens,
              completion_tokens,
              total_tokens,
              estimated_cost_usd,
              latency_ms,
              pricing_source,
              pricing_snapshot,
              error_message
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11::jsonb, $12)
            RETURNING id
            """,
            str(feature),
            str(status),
            requested_models,
            actual_model,
            prompt_tokens,
            completion_tokens,
            total_tokens,
            estimated_cost_usd,
            latency_ms,
            pricing_source,
            json.dumps(pricing_snapshot) if pricing_snapshot is not None else None,
            error_message,
        )
        return int(row["id"])


@dataclass(frozen=True)
class GeekNewsSummary:
    item_id: int
    summary: str
    model: str
    generated_at: datetime
