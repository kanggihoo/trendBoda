import logging
from dataclasses import dataclass
from typing import Protocol

from trendboda.exceptions import GeekNewsFetchFailed
from trendboda.services.geeknews import GeekNewsFetchService

logger = logging.getLogger(__name__)


class TelegramSenderProtocol(Protocol):
    async def send_message(self, *, chat_id: int, text: str) -> None: ...


@dataclass(frozen=True)
class ScheduledGeekNewsJobResult:
    fetched_count: int
    inserted_count: int
    pushed_count: int
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
                skipped_push_reason="Fetch failed",
                error_message=str(exc),
            )
        except Exception as exc:
            logger.exception("GeekNews scheduled fetch encountered unexpected error")
            return ScheduledGeekNewsJobResult(
                fetched_count=0,
                inserted_count=0,
                pushed_count=0,
                skipped_push_reason="Database or unexpected error",
                error_message=str(exc),
            )

        if fetch_result.inserted_count == 0:
            return ScheduledGeekNewsJobResult(
                fetched_count=fetch_result.fetched_count,
                inserted_count=0,
                pushed_count=0,
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
                skipped_push_reason=skipped_reason,
                error_message=None,
            )

        # Telegram push will be implemented here later
        pushed_count = 0
        skipped_push_reason = None
        
        return ScheduledGeekNewsJobResult(
            fetched_count=fetch_result.fetched_count,
            inserted_count=fetch_result.inserted_count,
            pushed_count=pushed_count,
            skipped_push_reason=skipped_push_reason,
            error_message=None,
        )
