import logging
from dataclasses import dataclass
from typing import Protocol

from trendboda.exceptions import GeekNewsFetchFailed
from trendboda.services.geeknews import GeekNewsFetchService
from trendboda.telegram_bot.messages import format_geeknews_message
from trendboda.telegram_bot.types import GeekNewsTelegramItem

logger = logging.getLogger(__name__)


class TelegramSenderProtocol(Protocol):
    async def send_message(self, *, chat_id: int, text: str) -> None: ...


@dataclass(frozen=True)
class ScheduledGeekNewsJobResult:
    fetched_count: int
    inserted_count: int
    pushed_count: int
    failed_push_count: int
    skipped_push_reason: str | None
    error_message: str | None


@dataclass(frozen=True)
class ScheduledGeekNewsJob:
    fetch_service: GeekNewsFetchService
    telegram_sender: TelegramSenderProtocol | None
    telegram_allowed_chat_ids: set[int]

    async def run_once(self) -> ScheduledGeekNewsJobResult:
        try:
            fetch_result = await self.fetch_service.fetch()
        except GeekNewsFetchFailed as exc:
            logger.exception("GeekNews scheduled fetch failed")
            return ScheduledGeekNewsJobResult(
                fetched_count=0,
                inserted_count=0,
                pushed_count=0,
                failed_push_count=0,
                skipped_push_reason="Fetch failed",
                error_message=str(exc),
            )
        except Exception as exc:
            logger.exception("GeekNews scheduled fetch encountered unexpected error")
            return ScheduledGeekNewsJobResult(
                fetched_count=0,
                inserted_count=0,
                pushed_count=0,
                failed_push_count=0,
                skipped_push_reason="Database or unexpected error",
                error_message=str(exc),
            )

        if fetch_result.inserted_count == 0:
            return ScheduledGeekNewsJobResult(
                fetched_count=fetch_result.fetched_count,
                inserted_count=0,
                pushed_count=0,
                failed_push_count=0,
                skipped_push_reason="No new items",
                error_message=None,
            )

        if self.telegram_sender is None or not self.telegram_allowed_chat_ids:
            skipped_reason = "Missing Telegram token or allowed chat ID"
            logger.info("GeekNews push skipped: %s", skipped_reason)
            return ScheduledGeekNewsJobResult(
                fetched_count=fetch_result.fetched_count,
                inserted_count=fetch_result.inserted_count,
                pushed_count=0,
                failed_push_count=0,
                skipped_push_reason=skipped_reason,
                error_message=None,
            )

        pushed_count = 0
        failed_push_count = 0

        for chat_id in self.telegram_allowed_chat_ids:
            for item in fetch_result.inserted_items:
                telegram_item = GeekNewsTelegramItem(
                    title=item.title,
                    source_url=item.source_url,
                    content_text=item.content_text,
                )
                text = format_geeknews_message([telegram_item])
                try:
                    await self.telegram_sender.send_message(chat_id=chat_id, text=text)
                    pushed_count += 1
                except Exception as exc:
                    logger.exception(
                        "Failed to send GeekNews Signal %d to Telegram chat %d: %s",
                        item.id,
                        chat_id,
                        exc,
                    )
                    failed_push_count += 1
        
        return ScheduledGeekNewsJobResult(
            fetched_count=fetch_result.fetched_count,
            inserted_count=fetch_result.inserted_count,
            pushed_count=pushed_count,
            failed_push_count=failed_push_count,
            skipped_push_reason=None,
            error_message=None,
        )
