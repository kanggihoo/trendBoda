import pytest

from trendboda.exceptions import GeekNewsFetchFailed
from trendboda.geeknews import StoredGeekNewsItem
from trendboda.services.geeknews import GeekNewsFetchResult
from trendboda.services.scheduled_geeknews import ScheduledGeekNewsJob


class FakeGeekNewsFetchService:
    def __init__(self, result: GeekNewsFetchResult | Exception) -> None:
        self.result = result

    async def fetch(self) -> GeekNewsFetchResult:
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class FakeTelegramSender:
    def __init__(self) -> None:
        self.messages: list[tuple[int, str]] = []
        self.fail_on_text: str | None = None

    async def send_message(self, *, chat_id: int, text: str) -> None:
        if self.fail_on_text and self.fail_on_text in text:
            raise RuntimeError("simulated send failure")
        self.messages.append((chat_id, text))


async def test_job_skips_push_when_no_new_items() -> None:
    fetch_service = FakeGeekNewsFetchService(
        GeekNewsFetchResult(
            fetch_run_id=1,
            fetched_count=5,
            inserted_count=0,
            inserted_items=[],
        )
    )
    job = ScheduledGeekNewsJob(
        fetch_service=fetch_service,  # type: ignore
        telegram_sender=FakeTelegramSender(),
        telegram_allowed_chat_ids={123},
    )

    result = await job.run_once()

    assert result.fetched_count == 5
    assert result.inserted_count == 0
    assert result.pushed_count == 0
    assert result.failed_push_count == 0
    assert result.skipped_push_reason == "No new items"
    assert result.error_message is None


async def test_job_skips_push_when_telegram_not_configured() -> None:
    fetch_service = FakeGeekNewsFetchService(
        GeekNewsFetchResult(
            fetch_run_id=1,
            fetched_count=5,
            inserted_count=2,
            inserted_items=[
                StoredGeekNewsItem(id=1, fetch_run_id=1, external_id="a", title="A", source_url="a", content_text="a", published_at=None, fetched_at=None),  # type: ignore
                StoredGeekNewsItem(id=2, fetch_run_id=1, external_id="b", title="B", source_url="b", content_text="b", published_at=None, fetched_at=None),  # type: ignore
            ],
        )
    )
    job = ScheduledGeekNewsJob(
        fetch_service=fetch_service,  # type: ignore
        telegram_sender=None,
        telegram_allowed_chat_ids={123},
    )

    result = await job.run_once()

    assert result.fetched_count == 5
    assert result.inserted_count == 2
    assert result.pushed_count == 0
    assert result.failed_push_count == 0
    assert result.skipped_push_reason == "Missing Telegram token or allowed chat ID"


async def test_job_returns_failure_result_on_fetch_error() -> None:
    fetch_service = FakeGeekNewsFetchService(GeekNewsFetchFailed("upstream down"))
    job = ScheduledGeekNewsJob(
        fetch_service=fetch_service,  # type: ignore
        telegram_sender=FakeTelegramSender(),
        telegram_allowed_chat_ids={123},
    )

    result = await job.run_once()

    assert result.fetched_count == 0
    assert result.inserted_count == 0
    assert result.pushed_count == 0
    assert result.failed_push_count == 0
    assert result.skipped_push_reason == "Fetch failed"
    assert "upstream down" in str(result.error_message)


async def test_job_returns_failure_result_on_database_error() -> None:
    fetch_service = FakeGeekNewsFetchService(RuntimeError("db connection failed"))
    job = ScheduledGeekNewsJob(
        fetch_service=fetch_service,  # type: ignore
        telegram_sender=FakeTelegramSender(),
        telegram_allowed_chat_ids={123},
    )

    result = await job.run_once()

    assert result.fetched_count == 0
    assert result.inserted_count == 0
    assert result.pushed_count == 0
    assert result.failed_push_count == 0
    assert result.skipped_push_reason == "Database or unexpected error"
    assert "db connection failed" in str(result.error_message)


async def test_job_pushes_every_new_item() -> None:
    fetch_service = FakeGeekNewsFetchService(
        GeekNewsFetchResult(
            fetch_run_id=1,
            fetched_count=5,
            inserted_count=2,
            inserted_items=[
                StoredGeekNewsItem(id=1, fetch_run_id=1, external_id="a", title="Title A", source_url="urlA", content_text="bodyA", published_at=None, fetched_at=None),  # type: ignore
                StoredGeekNewsItem(id=2, fetch_run_id=1, external_id="b", title="Title B", source_url="urlB", content_text="bodyB", published_at=None, fetched_at=None),  # type: ignore
            ],
        )
    )
    sender = FakeTelegramSender()
    job = ScheduledGeekNewsJob(
        fetch_service=fetch_service,  # type: ignore
        telegram_sender=sender,
        telegram_allowed_chat_ids={123},
    )

    result = await job.run_once()

    assert result.pushed_count == 2
    assert result.failed_push_count == 0
    assert len(sender.messages) == 2
    assert "Title A" in sender.messages[0][1]
    assert "Title B" in sender.messages[1][1]


async def test_job_isolates_per_message_failures() -> None:
    fetch_service = FakeGeekNewsFetchService(
        GeekNewsFetchResult(
            fetch_run_id=1,
            fetched_count=5,
            inserted_count=3,
            inserted_items=[
                StoredGeekNewsItem(id=1, fetch_run_id=1, external_id="a", title="Title A", source_url="urlA", content_text="bodyA", published_at=None, fetched_at=None),  # type: ignore
                StoredGeekNewsItem(id=2, fetch_run_id=1, external_id="bad", title="Bad Title", source_url="urlBad", content_text="bodyBad", published_at=None, fetched_at=None),  # type: ignore
                StoredGeekNewsItem(id=3, fetch_run_id=1, external_id="c", title="Title C", source_url="urlC", content_text="bodyC", published_at=None, fetched_at=None),  # type: ignore
            ],
        )
    )
    sender = FakeTelegramSender()
    sender.fail_on_text = "Bad Title"
    job = ScheduledGeekNewsJob(
        fetch_service=fetch_service,  # type: ignore
        telegram_sender=sender,
        telegram_allowed_chat_ids={123},
    )

    result = await job.run_once()

    assert result.pushed_count == 2
    assert result.failed_push_count == 1
    assert len(sender.messages) == 2
    assert "Title A" in sender.messages[0][1]
    assert "Title C" in sender.messages[1][1]
