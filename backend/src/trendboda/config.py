from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    database_url: str = Field(default="postgres://trendboda:trendboda@localhost:5432/trendboda")
    openrouter_api_key: str | None = None
    telegram_bot_token: str | None = None
    telegram_allowed_chat_ids: str = ""
    ai_monthly_budget_usd: str = Field(default="10.00")
    geeknews_scheduler_interval_seconds: int = Field(default=7200)

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def telegram_allowed_chat_ids_set(self) -> set[int]:
        raw_value = self.telegram_allowed_chat_ids.strip()
        if not raw_value or raw_value == "...":
            return set()
        return {
            int(raw_chat_id.strip())
            for raw_chat_id in raw_value.split(",")
            if raw_chat_id.strip()
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
