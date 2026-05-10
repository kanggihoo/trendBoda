import asyncio
import logging
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from typing import Protocol, cast

import httpx

from trendboda import database
from trendboda.config import get_settings
from trendboda.geeknews import StoredGeekNewsItem
from trendboda.repositories import GeekNewsSummary, Repositories

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TelegramMessage:
    chat_id: int
    text: str


@dataclass(frozen=True)
class GeekNewsTelegramItem:
    title: str
    source_url: str
    summary: str | None


class TelegramGeekNewsRepository(Protocol):
    async def list_recent_items(self, *, limit: int) -> list[StoredGeekNewsItem]: ...

    async def get_summary(self, *, item_id: int) -> GeekNewsSummary | None: ...


class TelegramAIUsageRepository(Protocol):
    async def summarize_ai_cost(self, *, monthly_budget_usd: str) -> dict[str, object]: ...


class TelegramRepositories(Protocol):
    @property
    def geeknews(self) -> TelegramGeekNewsRepository: ...

    @property
    def ai_usage(self) -> TelegramAIUsageRepository: ...


class TelegramInteractiveBot:
    def __init__(
        self,
        *,
        allowed_chat_ids: set[int],
        repositories: TelegramRepositories | None = None,
    ) -> None:
        self._allowed_chat_ids = allowed_chat_ids
        self._repositories = repositories

    async def handle_update(self, update: Mapping[str, object]) -> dict[str, object] | None:
        message = _dict_or_none(update.get("message"))
        if message is None:
            return None

        chat = _dict_or_none(message.get("chat"))
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
            summary = await self._repositories.geeknews.get_summary(item_id=item.id)
            telegram_items.append(
                GeekNewsTelegramItem(
                    title=item.title,
                    source_url=item.source_url,
                    summary=summary.summary if summary is not None else None,
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


class TelegramPollingRunner:
    def __init__(self, *, token: str, bot: TelegramInteractiveBot) -> None:
        self._bot = bot
        self._base_url = f"https://api.telegram.org/bot{token}"

    async def poll_once(self, *, offset: int | None = None) -> int | None:
        params: dict[str, int] = {"timeout": 25}
        if offset is not None:
            params["offset"] = offset

        async with httpx.AsyncClient(base_url=self._base_url, timeout=30) as client:
            response = await client.get("/getUpdates", params=params)
            response.raise_for_status()
            payload = _dict_or_none(response.json())
            if payload is None:
                return offset
            updates = payload.get("result", [])
            if not isinstance(updates, list):
                return offset
            updates = cast(list[object], updates)

            next_offset = offset
            for update_object in updates:
                update = _dict_or_none(update_object)
                if update is None:
                    continue

                update_id = update.get("update_id")
                if isinstance(update_id, int):
                    next_offset = update_id + 1

                outgoing = await self._bot.handle_update(update)
                if outgoing is not None:
                    await client.post("/sendMessage", json=outgoing)

        return next_offset

    async def run_forever(self) -> None:
        offset: int | None = None
        while True:
            try:
                offset = await self.poll_once(offset=offset)
            except httpx.HTTPError:
                logger.exception("Telegram polling request failed")
                await asyncio.sleep(5)


def build_polling_runner(
    *,
    repositories: TelegramRepositories | None = None,
) -> TelegramPollingRunner:
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")

    bot = TelegramInteractiveBot(
        allowed_chat_ids=settings.telegram_allowed_chat_ids_set,
        repositories=repositories,
    )
    return TelegramPollingRunner(token=settings.telegram_bot_token, bot=bot)


async def run_polling() -> None:
    settings = get_settings()
    pool = await database.create_pool(settings.database_url)
    try:
        runner = build_polling_runner(repositories=Repositories(pool=pool))
        logger.info("Starting TrendBoda Interactive Bot polling")
        await runner.run_forever()
    finally:
        await pool.close()


def main() -> None:
    configure_logging()
    try:
        asyncio.run(run_polling())
    except KeyboardInterrupt:
        logger.info("Stopped TrendBoda Interactive Bot polling")


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)


def format_geeknews_message(items: list[GeekNewsTelegramItem]) -> str:
    if not items:
        return "No recent Developer Trend Source signals."

    lines = ["Recent Developer Trend Source signals"]
    for index, item in enumerate(items, start=1):
        lines.append(f"{index}. {item.title}")
        if item.summary is not None:
            lines.append(item.summary)
        lines.append(item.source_url)
    return "\n".join(lines)


def format_cost_message(summary: Mapping[str, object], *, monthly_budget_usd: str) -> str:
    totals = _dict_or_none(summary.get("totals")) or {}
    budget = _dict_or_none(summary.get("budget")) or {}
    return "\n".join(
        [
            "OpenRouter cost",
            (
                f"Total: ${totals.get('estimated_cost_usd', '0')} across "
                f"{totals.get('request_count', 0)} requests"
            ),
            (
                f"Month: ${budget.get('estimated_monthly_cost_usd', '0')} / "
                f"${budget.get('monthly_budget_usd', monthly_budget_usd)} "
                f"({budget.get('percent_used', '0')}%)"
            ),
            f"Failures: {totals.get('failure_count', 0)}",
        ]
    )


def _dict_or_none(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None
    return cast(dict[str, object], value)


if __name__ == "__main__":
    main()
