import pytest

from trendboda.config import ROOT_DIR, Settings, get_settings


def test_root_dir_points_to_repo_root() -> None:
    assert (ROOT_DIR / "AGENTS.md").exists()


def test_settings_reads_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@localhost:5432/testdb")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("AI_MONTHLY_BUDGET_USD", "25.50")

    settings = Settings()

    assert settings.database_url == "postgres://user:pass@localhost:5432/testdb"
    assert settings.openrouter_api_key == "test-key"
    assert settings.ai_monthly_budget_usd == "25.50"


def test_get_settings_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@localhost:5432/testdb")

    first = get_settings()
    second = get_settings()

    assert first is second
