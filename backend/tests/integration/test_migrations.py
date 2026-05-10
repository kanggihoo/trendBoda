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
        columns = await connection.fetch(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'geeknews_items'
              AND column_name IN (
                'content_raw_html',
                'content_text'
              )
            ORDER BY column_name
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
    assert [row["column_name"] for row in columns] == ["content_raw_html", "content_text"]
