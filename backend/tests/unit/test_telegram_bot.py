import logging
from datetime import UTC, datetime

import pytest
import respx
from httpx import Response

from trendboda.geeknews import StoredGeekNewsItem
from trendboda.repositories import GeekNewsSummary
from trendboda.telegram_bot import (
    GeekNewsTelegramItem,
    TelegramInteractiveBot,
    TelegramPollingRunner,
    TelegramSender,
    build_polling_runner,
    configure_logging,
    format_cost_message,
    format_geeknews_message,
)


class FakeGeekNewsRepository:
    async def list_recent_items(self, *, limit: int) -> list[StoredGeekNewsItem]:
        return [
            StoredGeekNewsItem(
                id=1,
                fetch_run_id=10,
                external_id="item-1",
                title="Stored signal",
                source_url="https://news.example.com/1",
                content_text="Stored item body",
                published_at=datetime(2026, 5, 9, 10, 0, tzinfo=UTC),
                fetched_at=datetime(2026, 5, 9, 10, 5, tzinfo=UTC),
            )
        ][:limit]

    async def get_summary(self, *, item_id: int) -> GeekNewsSummary | None:
        if item_id != 1:
            return None
        return GeekNewsSummary(
            item_id=1,
            summary="Existing stored summary",
            model="openai/gpt-4.1-nano",
            generated_at=datetime(2026, 5, 9, 10, 6, tzinfo=UTC),
        )


class FakeRepositories:
    def __init__(self) -> None:
        self.geeknews = FakeGeekNewsRepository()
        self.ai_usage = FakeAIUsageRepository()


class FakeAIUsageRepository:
    async def summarize_ai_cost(self, *, monthly_budget_usd: str) -> dict[str, object]:
        return {
            "totals": {
                "estimated_cost_usd": "0.0085",
                "request_count": 3,
                "success_count": 2,
                "failure_count": 1,
                "average_latency_ms": 150,
            },
            "budget": {
                "monthly_budget_usd": monthly_budget_usd,
                "estimated_monthly_cost_usd": "0.006",
                "percent_used": "0.06",
            },
        }


class EmptyAIUsageRepository:
    async def summarize_ai_cost(self, *, monthly_budget_usd: str) -> dict[str, object]:
        return {
            "totals": {
                "estimated_cost_usd": "0",
                "request_count": 0,
                "success_count": 0,
                "failure_count": 0,
                "average_latency_ms": None,
            },
            "budget": {
                "monthly_budget_usd": monthly_budget_usd,
                "estimated_monthly_cost_usd": "0",
                "percent_used": "0",
            },
        }


class EmptyGeekNewsRepository(FakeGeekNewsRepository):
    async def list_recent_items(self, *, limit: int) -> list[StoredGeekNewsItem]:
        return []


class FailingGeekNewsRepository(FakeGeekNewsRepository):
    async def list_recent_items(self, *, limit: int) -> list[StoredGeekNewsItem]:
        raise RuntimeError("database unavailable")


class EmptyRepositories(FakeRepositories):
    def __init__(self) -> None:
        self.geeknews = EmptyGeekNewsRepository()
        self.ai_usage = EmptyAIUsageRepository()


class FailingRepositories(FakeRepositories):
    def __init__(self) -> None:
        self.geeknews = FailingGeekNewsRepository()
        self.ai_usage = FakeAIUsageRepository()


def test_format_geeknews_message_is_concise_and_mobile_friendly() -> None:
    message = format_geeknews_message(
        [
            GeekNewsTelegramItem(
                title="Stored signal",
                source_url="https://news.example.com/1",
                summary="Existing stored summary",
            )
        ]
    )

    assert message == (
        "Recent Developer Trend Source signals\n"
        "1. Stored signal\n"
        "Existing stored summary\n"
        "https://news.example.com/1"
    )


def test_format_cost_message_is_concise_and_mobile_friendly() -> None:
    message = format_cost_message(
        {
            "totals": {
                "estimated_cost_usd": "0.0085",
                "request_count": 3,
                "failure_count": 1,
            },
            "budget": {
                "monthly_budget_usd": "10.00",
                "estimated_monthly_cost_usd": "0.006",
                "percent_used": "0.06",
            },
        },
        monthly_budget_usd="10.00",
    )

    assert message == (
        "OpenRouter cost\n"
        "Total: $0.0085 across 3 requests\n"
        "Month: $0.006 / $10.00 (0.06%)\n"
        "Failures: 1"
    )


@pytest.mark.asyncio
async def test_interactive_bot_logs_chat_id_when_allowlist_is_empty(caplog) -> None:
    bot = TelegramInteractiveBot(allowed_chat_ids=set())
    update = {
        "message": {
            "chat": {"id": 123456789},
            "text": "/start",
        }
    }

    with caplog.at_level(logging.INFO):
        result = await bot.handle_update(update)

    assert result == {
        "chat_id": 123456789,
        "text": "TrendBoda ready. chat_id=123456789",
    }
    assert "Telegram message from chat_id=123456789" in caplog.text


@pytest.mark.asyncio
async def test_geeknews_command_returns_recent_signals_with_summary_and_link() -> None:
    bot = TelegramInteractiveBot(allowed_chat_ids={123456789}, repositories=FakeRepositories())

    result = await bot.handle_update(
        {
            "message": {
                "chat": {"id": 123456789},
                "text": "/geeknews",
            }
        }
    )

    assert result == {
        "chat_id": 123456789,
        "text": (
            "Recent Developer Trend Source signals\n"
            "1. Stored signal\n"
            "Existing stored summary\n"
            "https://news.example.com/1"
        ),
    }


@pytest.mark.asyncio
async def test_cost_command_returns_openrouter_spend_summary() -> None:
    bot = TelegramInteractiveBot(allowed_chat_ids={123456789}, repositories=FakeRepositories())

    result = await bot.handle_update(
        {
            "message": {
                "chat": {"id": 123456789},
                "text": "/cost",
            }
        }
    )

    assert result == {
        "chat_id": 123456789,
        "text": (
            "OpenRouter cost\n"
            "Total: $0.0085 across 3 requests\n"
            "Month: $0.006 / $10.00 (0.06%)\n"
            "Failures: 1"
        ),
    }


@pytest.mark.asyncio
async def test_geeknews_command_returns_empty_state() -> None:
    bot = TelegramInteractiveBot(allowed_chat_ids={123456789}, repositories=EmptyRepositories())

    result = await bot.handle_update(
        {
            "message": {
                "chat": {"id": 123456789},
                "text": "/geeknews",
            }
        }
    )

    assert result == {
        "chat_id": 123456789,
        "text": "No recent Developer Trend Source signals.",
    }


@pytest.mark.asyncio
async def test_cost_command_returns_empty_usage_state() -> None:
    bot = TelegramInteractiveBot(allowed_chat_ids={123456789}, repositories=EmptyRepositories())

    result = await bot.handle_update(
        {
            "message": {
                "chat": {"id": 123456789},
                "text": "/cost",
            }
        }
    )

    assert result == {
        "chat_id": 123456789,
        "text": (
            "OpenRouter cost\n"
            "Total: $0 across 0 requests\n"
            "Month: $0 / $10.00 (0%)\n"
            "Failures: 0"
        ),
    }


@pytest.mark.asyncio
async def test_geeknews_command_handles_backend_failure() -> None:
    bot = TelegramInteractiveBot(allowed_chat_ids={123456789}, repositories=FailingRepositories())

    result = await bot.handle_update(
        {
            "message": {
                "chat": {"id": 123456789},
                "text": "/geeknews",
            }
        }
    )

    assert result == {
        "chat_id": 123456789,
        "text": "TrendBoda data is unavailable. Try again later.",
    }


@pytest.mark.asyncio
async def test_interactive_bot_rejects_unknown_chat() -> None:
    bot = TelegramInteractiveBot(allowed_chat_ids={123456789}, repositories=FakeRepositories())

    result = await bot.handle_update(
        {
            "message": {
                "chat": {"id": 999},
                "text": "/geeknews",
            }
        }
    )

    assert result == {
        "chat_id": 999,
        "text": "This TrendBoda Interactive Bot is owner-only.",
    }


@pytest.mark.asyncio
async def test_polling_runner_replies_with_chat_id_for_start_command() -> None:
    bot = TelegramInteractiveBot(allowed_chat_ids=set())
    runner = TelegramPollingRunner(token="test-token", bot=bot)

    with respx.mock(base_url="https://api.telegram.org") as api:
        get_updates = api.get("/bottest-token/getUpdates").mock(
            return_value=Response(
                200,
                json={
                    "ok": True,
                    "result": [
                        {
                            "update_id": 10,
                            "message": {
                                "chat": {"id": 123456789},
                                "text": "/start",
                            },
                        }
                    ],
                },
            )
        )
        send_message = api.post("/bottest-token/sendMessage").mock(
            return_value=Response(200, json={"ok": True, "result": {}})
        )

        next_offset = await runner.poll_once()

    assert next_offset == 11
    assert "timeout=25" in str(get_updates.calls.last.request.url)
    assert send_message.called
    assert send_message.calls.last.request.content == (
        b'{"chat_id":123456789,"text":"TrendBoda ready. chat_id=123456789"}'
    )


def test_configure_logging_suppresses_httpx_request_urls() -> None:
    configure_logging()

    assert logging.getLogger("httpx").level == logging.WARNING


@pytest.mark.asyncio
async def test_sender_posts_message_to_owner_chat() -> None:
    sender = TelegramSender(token="test-token")

    with respx.mock(base_url="https://api.telegram.org") as api:
        send_message = api.post("/bottest-token/sendMessage").mock(
            return_value=Response(200, json={"ok": True, "result": {}})
        )

        await sender.send_message(chat_id=123456789, text="TrendBoda smoke message")

    assert send_message.calls.last.request.content == (
        b'{"chat_id":123456789,"text":"TrendBoda smoke message"}'
    )


@pytest.mark.asyncio
async def test_build_polling_runner_can_use_repositories_for_commands(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_ALLOWED_CHAT_IDS", "123456789")
    runner = build_polling_runner(repositories=FakeRepositories())

    with respx.mock(base_url="https://api.telegram.org") as api:
        api.get("/bottest-token/getUpdates").mock(
            return_value=Response(
                200,
                json={
                    "ok": True,
                    "result": [
                        {
                            "update_id": 10,
                            "message": {
                                "chat": {"id": 123456789},
                                "text": "/geeknews",
                            },
                        }
                    ],
                },
            )
        )
        send_message = api.post("/bottest-token/sendMessage").mock(
            return_value=Response(200, json={"ok": True, "result": {}})
        )

        await runner.poll_once()

    assert b"Stored signal" in send_message.calls.last.request.content
