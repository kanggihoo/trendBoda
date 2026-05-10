import asyncpg
import pytest


@pytest.mark.integration
async def test_geeknews_tables_are_created(migrated_database_url: str) -> None:
    connection = await asyncpg.connect(migrated_database_url)
    try:
        rows = await connection.fetch(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name IN (
                'ai_usage_records',
                'geeknews_fetch_runs',
                'geeknews_items',
                'geeknews_summaries'
              )
            ORDER BY table_name
            """
        )
    finally:
        await connection.close()

    assert [row["table_name"] for row in rows] == [
        "ai_usage_records",
        "geeknews_fetch_runs",
        "geeknews_items",
        "geeknews_summaries",
    ]
