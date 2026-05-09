from datetime import UTC, datetime

import asyncpg
import pytest

from trendboda.geeknews import GeekNewsItem
from trendboda.repositories import GeekNewsRepository


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
            published_at=datetime(2026, 5, 9, 10, 0, tzinfo=UTC),
        )

        first_count = await repository.upsert_items(fetch_run_id=run_id, items=[item])
        second_count = await repository.upsert_items(fetch_run_id=run_id, items=[item])
        recent_items = await repository.list_recent_items(limit=10)

        assert first_count == 1
        assert second_count == 0
        assert len(recent_items) == 1
        assert recent_items[0].title == "First signal"
        assert recent_items[0].fetch_run_id == run_id
    finally:
        await pool.close()
