import argparse
import asyncio
import logging
import sys

from trendboda.bootstrap import bootstrap_application
from trendboda.config import get_settings
from trendboda.services.scheduled_geeknews import ScheduledGeekNewsJob

logger = logging.getLogger(__name__)


async def run_once() -> int:
    async with bootstrap_application() as container:
        job = ScheduledGeekNewsJob(
            fetch_service=container.geeknews_fetch_service,
            telegram_sender=container.telegram_sender,
            telegram_allowed_chat_ids=container.settings.telegram_allowed_chat_ids_set,
        )
        logger.info("Running scheduled GeekNews job once")
        result = await job.run_once()
        
        logger.info(
            "GeekNews job finished: fetched=%d, inserted=%d, pushed=%d, failed_push=%d, skipped=%s",
            result.fetched_count,
            result.inserted_count,
            result.pushed_count,
            result.failed_push_count,
            result.skipped_push_reason,
        )
        
        if result.error_message is not None:
            logger.error("Job encountered a critical error: %s", result.error_message)
            return 1
            
        return 0


async def run_forever(sleep_fn=asyncio.sleep) -> None:
    settings = get_settings()
    interval = settings.geeknews_scheduler_interval_seconds
    
    async with bootstrap_application() as container:
        job = ScheduledGeekNewsJob(
            fetch_service=container.geeknews_fetch_service,
            telegram_sender=container.telegram_sender,
            telegram_allowed_chat_ids=container.settings.telegram_allowed_chat_ids_set,
        )
        
        logger.info("Starting scheduled GeekNews job loop, interval=%ds", interval)
        while True:
            try:
                result = await job.run_once()
                logger.info(
                    "GeekNews job finished: fetched=%d, inserted=%d, pushed=%d, failed_push=%d, skipped=%s",
                    result.fetched_count,
                    result.inserted_count,
                    result.pushed_count,
                    result.failed_push_count,
                    result.skipped_push_reason,
                )
            except asyncio.CancelledError:
                logger.info("Scheduler interrupted")
                raise
            except Exception as exc:
                logger.exception("Unexpected error in scheduler loop: %s", exc)
                
            await sleep_fn(interval)


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    configure_logging()
    
    parser = argparse.ArgumentParser(description="TrendBoda Scheduler")
    parser.add_argument(
        "mode",
        choices=["run-once", "run-forever"],
        help="Scheduler mode: run once and exit, or run forever on an interval",
    )
    args = parser.parse_args()
    
    try:
        if args.mode == "run-once":
            exit_code = asyncio.run(run_once())
            sys.exit(exit_code)
        elif args.mode == "run-forever":
            asyncio.run(run_forever())
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")


if __name__ == "__main__":
    main()
