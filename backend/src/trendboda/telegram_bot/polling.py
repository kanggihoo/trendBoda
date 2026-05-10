import asyncio
import logging
from typing import cast

import httpx

from trendboda.config import get_settings
from trendboda.telegram_bot.interactive_bot import TelegramInteractiveBot
from trendboda.telegram_bot.messages import dict_or_none
from trendboda.telegram_bot.sender import TelegramSender
from trendboda.telegram_bot.types import TelegramRepositories

logger = logging.getLogger(__name__)


class TelegramPollingRunner:
    def __init__(
        self,
        *,
        token: str,
        bot: TelegramInteractiveBot,
        sender: TelegramSender | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._bot = bot
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(
            base_url=f"https://api.telegram.org/bot{token}",
            timeout=30,
        )
        self._sender = sender or TelegramSender(token=token, http_client=self._client)

    async def poll_once(self, *, offset: int | None = None) -> int | None:
        params: dict[str, int] = {"timeout": 25}
        if offset is not None:
            params["offset"] = offset

        response = await self._client.get("/getUpdates", params=params)
        response.raise_for_status()
        payload = dict_or_none(response.json())
        if payload is None:
            return offset
        updates = payload.get("result", [])
        if not isinstance(updates, list):
            return offset
        updates = cast(list[object], updates)

        next_offset = offset
        for update_object in updates:
            update = dict_or_none(update_object)
            if update is None:
                continue

            update_id = update.get("update_id")
            if isinstance(update_id, int):
                next_offset = update_id + 1

            outgoing = await self._bot.handle_update(update)
            if outgoing is not None:
                await self._sender.send_payload(outgoing)

        return next_offset

    async def run_forever(self) -> None:
        offset: int | None = None
        while True:
            try:
                offset = await self.poll_once(offset=offset)
            except httpx.HTTPError:
                logger.exception("Telegram polling request failed")
                await asyncio.sleep(5)

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()


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
