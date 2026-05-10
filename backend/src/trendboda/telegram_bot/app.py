import asyncio
import logging

from trendboda import database
from trendboda.config import get_settings
from trendboda.repositories import Repositories
from trendboda.telegram_bot.polling import build_polling_runner

logger = logging.getLogger(__name__)


async def run_polling() -> None:
    settings = get_settings()
    pool = await database.create_pool(settings.database_url)
    runner = None
    try:
        runner = build_polling_runner(repositories=Repositories(pool=pool))
        logger.info("Starting TrendBoda Interactive Bot polling")
        await runner.run_forever()
    finally:
        if runner is not None:
            await runner.aclose()
        await pool.close()


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    configure_logging()
    try:
        asyncio.run(run_polling())
    except KeyboardInterrupt:
        logger.info("Stopped TrendBoda Interactive Bot polling")
