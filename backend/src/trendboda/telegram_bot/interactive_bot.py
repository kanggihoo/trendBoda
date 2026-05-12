import logging
from collections.abc import Awaitable, Callable

from trendboda.config import get_settings
from trendboda.telegram_bot.messages import (
    dict_or_none,
    format_cost_message,
    format_geeknews_message,
)
from trendboda.telegram_bot.types import (
    GeekNewsTelegramItem,
    TelegramOutgoingPayload,
    TelegramRepositories,
    TelegramUpdate,
)

logger = logging.getLogger(__name__)


class TelegramInteractiveBot:
    def __init__(
        self,
        *,
        allowed_chat_ids: set[int],
        repositories: TelegramRepositories | None = None,
    ) -> None:
        self._allowed_chat_ids = allowed_chat_ids
        self._repositories = repositories

    async def handle_update(self, update: TelegramUpdate) -> TelegramOutgoingPayload | None:
        message = dict_or_none(update.get("message"))
        if message is None:
            return None

        chat = dict_or_none(message.get("chat"))
        if chat is None:
            return None

        chat_id = chat.get("id")
        if not isinstance(chat_id, int):
            return None

        logger.info("Telegram message from chat_id=%s", chat_id)
        if self._allowed_chat_ids and chat_id not in self._allowed_chat_ids:
            return {
                "chat_id": chat_id,
                "text": "This TrendBoda Interactive Bot is owner-only.",
            }

        text = message.get("text")
        if text == "/start":
            return {
                "chat_id": chat_id,
                "text": f"TrendBoda ready. chat_id={chat_id}",
            }
        if text == "/geeknews":
            return {
                "chat_id": chat_id,
                "text": await self._format_command(self._format_geeknews),
            }
        if text == "/cost":
            return {
                "chat_id": chat_id,
                "text": await self._format_command(self._format_cost),
            }

        return None

    async def _format_command(self, formatter: Callable[[], Awaitable[str]]) -> str:
        try:
            return await formatter()
        except Exception:
            logger.exception("Telegram command failed")
            return "TrendBoda data is unavailable. Try again later."

    async def _format_geeknews(self) -> str:
        if self._repositories is None:
            return "TrendBoda data is unavailable."

        items = await self._repositories.geeknews.list_recent_items(limit=5)
        if not items:
            return "No recent Developer Trend Source signals."

        telegram_items: list[GeekNewsTelegramItem] = []
        for item in items:
            telegram_items.append(
                GeekNewsTelegramItem(
                    title=item.title,
                    source_url=item.source_url,
                    content_text=item.content_text,
                )
            )
        return format_geeknews_message(telegram_items)

    async def _format_cost(self) -> str:
        if self._repositories is None:
            return "TrendBoda data is unavailable."

        settings = get_settings()
        summary = await self._repositories.ai_usage.summarize_ai_cost(
            monthly_budget_usd=settings.ai_monthly_budget_usd
        )
        return format_cost_message(summary, monthly_budget_usd=settings.ai_monthly_budget_usd)
