import pytest

from trendboda.config import ROOT_DIR, Settings, get_settings


def test_root_dir_points_to_repo_root() -> None:
    assert (ROOT_DIR / "AGENTS.md").exists()


def test_settings_reads_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@localhost:5432/testdb")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("FINNHUB_API_KEY", "finnhub-test-key")
    monkeypatch.setenv("MARKET_WATCHLIST_SYMBOLS", "aapl, nvda, tsla")
    monkeypatch.setenv("AI_MONTHLY_BUDGET_USD", "25.50")
    monkeypatch.setenv("TELEGRAM_ALLOWED_CHAT_IDS", "123, 456")

    settings = Settings()

    assert settings.database_url == "postgres://user:pass@localhost:5432/testdb"
    assert settings.openrouter_api_key == "test-key"
    assert settings.finnhub_api_key == "finnhub-test-key"
    assert settings.market_watchlist_symbol_list == ["AAPL", "NVDA", "TSLA"]
    assert settings.ai_monthly_budget_usd == "25.50"
    assert settings.telegram_allowed_chat_ids_set == {123, 456}


def test_settings_treats_placeholder_chat_ids_as_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_ALLOWED_CHAT_IDS", "...")

    settings = Settings()

    assert settings.telegram_allowed_chat_ids_set == set()


def test_settings_defaults_market_watchlist_symbols() -> None:
    settings = Settings()

    assert settings.market_watchlist_symbol_list == ["AAPL", "NVDA", "TSLA"]


def test_get_settings_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@localhost:5432/testdb")

    first = get_settings()
    second = get_settings()

    assert first is second
