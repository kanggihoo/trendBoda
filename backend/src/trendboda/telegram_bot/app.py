import asyncio
import logging

from trendboda.bootstrap import bootstrap_application
from trendboda.telegram_bot.polling import build_polling_runner

logger = logging.getLogger(__name__)


async def run_polling() -> None:
    async with bootstrap_application() as container:
        runner = None
        try:
            runner = build_polling_runner(repositories=container.repositories)
            logger.info("Starting TrendBoda Interactive Bot polling")
            await runner.run_forever()
        finally:
            if runner is not None:
                await runner.aclose()


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    configure_logging()
    try:
        asyncio.run(run_polling())
    except KeyboardInterrupt:
        logger.info("Stopped TrendBoda Interactive Bot polling")
