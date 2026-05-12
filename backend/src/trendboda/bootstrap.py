from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from trendboda import database
from trendboda.config import Settings, get_settings
from trendboda.geeknews.provider import GeekNewsProvider
from trendboda.repositories import Repositories
from trendboda.services.geeknews import GeekNewsFetchService
from trendboda.telegram_bot.sender import TelegramSender


@dataclass
class ApplicationContainer:
    settings: Settings
    pool: Any  # asyncpg.Pool or equivalent
    repositories: Repositories
    geeknews_provider: GeekNewsProvider
    geeknews_fetch_service: GeekNewsFetchService
    telegram_sender: TelegramSender | None

    async def aclose(self) -> None:
        if self.telegram_sender is not None:
            await self.telegram_sender.aclose()
        await self.pool.close()


@asynccontextmanager
async def bootstrap_application() -> AsyncGenerator[ApplicationContainer]:
    settings = get_settings()
    pool = await database.create_pool(settings.database_url)
    repositories = Repositories(pool=pool)
    geeknews_provider = GeekNewsProvider()
    geeknews_fetch_service = GeekNewsFetchService(
        repository=repositories.geeknews,
        provider=geeknews_provider,
    )
    
    telegram_sender = None
    if settings.telegram_bot_token:
        telegram_sender = TelegramSender(token=settings.telegram_bot_token)
        
    container = ApplicationContainer(
        settings=settings,
        pool=pool,
        repositories=repositories,
        geeknews_provider=geeknews_provider,
        geeknews_fetch_service=geeknews_fetch_service,
        telegram_sender=telegram_sender,
    )
    
    try:
        yield container
    finally:
        await container.aclose()
