import asyncio
from unittest.mock import AsyncMock, patch

from trendboda.scheduler import run_forever, run_once
from trendboda.services.scheduled_geeknews import ScheduledGeekNewsJobResult


@patch("trendboda.scheduler.bootstrap_application")
@patch("trendboda.scheduler.ScheduledGeekNewsJob")
async def test_run_once_returns_zero_on_success(mock_job_class, mock_bootstrap) -> None:
    mock_container = AsyncMock()
    mock_container.settings.telegram_allowed_chat_ids_set = {123}
    mock_bootstrap.return_value.__aenter__.return_value = mock_container
    
    mock_job = AsyncMock()
    mock_job.run_once.return_value = ScheduledGeekNewsJobResult(
        fetched_count=5,
        inserted_count=2,
        pushed_count=2,
        failed_push_count=0,
        skipped_push_reason=None,
        error_message=None,
    )
    mock_job_class.return_value = mock_job

    exit_code = await run_once()

    assert exit_code == 0
    mock_job.run_once.assert_awaited_once()


@patch("trendboda.scheduler.bootstrap_application")
@patch("trendboda.scheduler.ScheduledGeekNewsJob")
async def test_run_once_returns_non_zero_on_critical_error(mock_job_class, mock_bootstrap) -> None:
    mock_container = AsyncMock()
    mock_container.settings.telegram_allowed_chat_ids_set = {123}
    mock_bootstrap.return_value.__aenter__.return_value = mock_container
    
    mock_job = AsyncMock()
    mock_job.run_once.return_value = ScheduledGeekNewsJobResult(
        fetched_count=0,
        inserted_count=0,
        pushed_count=0,
        failed_push_count=0,
        skipped_push_reason="Fetch failed",
        error_message="upstream unavailable",
    )
    mock_job_class.return_value = mock_job

    exit_code = await run_once()

    assert exit_code == 1
    mock_job.run_once.assert_awaited_once()


@patch("trendboda.scheduler.bootstrap_application")
@patch("trendboda.scheduler.ScheduledGeekNewsJob")
async def test_run_forever_loops_and_sleeps(mock_job_class, mock_bootstrap) -> None:
    mock_container = AsyncMock()
    mock_container.settings.telegram_allowed_chat_ids_set = {123}
    mock_bootstrap.return_value.__aenter__.return_value = mock_container
    
    mock_job = AsyncMock()
    mock_job.run_once.side_effect = [
        ScheduledGeekNewsJobResult(
            fetched_count=5,
            inserted_count=2,
            pushed_count=2,
            failed_push_count=0,
            skipped_push_reason=None,
            error_message=None,
        ),
        ScheduledGeekNewsJobResult(
            fetched_count=0,
            inserted_count=0,
            pushed_count=0,
            failed_push_count=0,
            skipped_push_reason="Fetch failed",
            error_message="upstream down",
        ),
        asyncio.CancelledError(),  # Break the infinite loop
    ]
    mock_job_class.return_value = mock_job
    
    sleep_calls = []
    async def fake_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)
        
    with patch("trendboda.scheduler.get_settings") as mock_get_settings:
        mock_get_settings.return_value.geeknews_scheduler_interval_seconds = 7200
        
        try:
            await run_forever(sleep_fn=fake_sleep)
        except asyncio.CancelledError:
            pass

    assert mock_job.run_once.await_count == 3
    assert sleep_calls == [7200, 7200]
