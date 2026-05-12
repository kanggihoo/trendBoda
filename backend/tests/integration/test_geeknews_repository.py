from datetime import UTC, datetime
from decimal import Decimal

import asyncpg
import pytest

from trendboda.ai import AIFeature, AIUsageStatus
from trendboda.geeknews import GeekNewsItem
from trendboda.repositories import AIUsageRepository, GeekNewsRepository


@pytest.mark.integration
async def test_geeknews_repository_records_fetch_and_prevents_duplicates(
    migrated_database_url: str,
) -> None:
    pool = await asyncpg.create_pool(migrated_database_url)
    try:
        repository = GeekNewsRepository(pool)
        run_id = await repository.record_fetch_run(status="success", item_count=1)
        item = GeekNewsItem(
            external_id="external-1",
            title="First signal",
            source_url="https://news.example.com/1",
            content_raw_html="<ul><li>First body</li></ul>",
            content_text="• First body",
            published_at=datetime(2026, 5, 9, 10, 0, tzinfo=UTC),
        )

        first_result = await repository.insert_new_items(fetch_run_id=run_id, items=[item])
        second_result = await repository.insert_new_items(fetch_run_id=run_id, items=[item])
        recent_items = await repository.list_recent_items(limit=10)

        assert first_result.inserted_count == 1
        assert len(first_result.inserted_items) == 1
        assert second_result.inserted_count == 0
        assert len(second_result.inserted_items) == 0
        assert len(recent_items) == 1
        assert recent_items[0].title == "First signal"
        assert recent_items[0].fetch_run_id == run_id
    finally:
        await pool.close()


@pytest.mark.integration
async def test_geeknews_repository_upserts_summary_and_records_ai_usage(
    migrated_database_url: str,
) -> None:
    pool = await asyncpg.create_pool(migrated_database_url)
    try:
        repository = GeekNewsRepository(pool)
        ai_usage_repository = AIUsageRepository(pool)
        run_id = await repository.record_fetch_run(status="success", item_count=1)
        await repository.insert_new_items(
            fetch_run_id=run_id,
            items=[
                GeekNewsItem(
                    external_id="external-summary",
                    title="Summary target",
                    source_url="https://news.example.com/summary",
                    content_raw_html="<ul><li>Summary body</li></ul>",
                    content_text="• Summary body",
                    published_at=datetime(2026, 5, 9, 10, 0, tzinfo=UTC),
                )
            ],
        )
        item = (await repository.list_recent_items(limit=1))[0]

        first = await repository.upsert_summary(
            item_id=item.id,
            summary="First summary",
            model="openai/gpt-4.1-nano",
        )
        second = await repository.upsert_summary(
            item_id=item.id,
            summary="Replacement summary",
            model="google/gemini-2.5-flash-lite",
        )
        usage_id = await ai_usage_repository.record_ai_usage(
            feature=AIFeature.GEEKNEWS_SUMMARY,
            status=AIUsageStatus.SUCCESS,
            requested_models=["openai/gpt-4.1-nano", "google/gemini-2.5-flash-lite"],
            actual_model="google/gemini-2.5-flash-lite",
            prompt_tokens=12,
            completion_tokens=6,
            total_tokens=18,
            estimated_cost_usd=Decimal("0.0000036"),
            latency_ms=25,
            pricing_source="openrouter",
            pricing_snapshot={"prompt": "0.10", "completion": "0.40"},
            error_message=None,
        )
        stored = await repository.get_summary(item_id=item.id)

        assert first.summary == "First summary"
        assert second.summary == "Replacement summary"
        assert stored is not None
        assert stored.summary == "Replacement summary"
        assert usage_id == 1
    finally:
        await pool.close()
