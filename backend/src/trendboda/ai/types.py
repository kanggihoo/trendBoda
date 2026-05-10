from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Any

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class AIFeature(StrEnum):
    GEEKNEWS_SUMMARY = "geeknews_summary"


class AIModel(StrEnum):
    OPENAI_GPT_4_1_NANO = "openai_gpt_4_1_nano"
    GOOGLE_GEMINI_2_5_FLASH_LITE = "google_gemini_2_5_flash_lite"


class AIUsageStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"


@dataclass(frozen=True)
class OpenRouterModelPricing:
    prompt_per_million: Decimal
    completion_per_million: Decimal
    source: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class OpenRouterResult:
    status: AIUsageStatus
    content: str | None
    actual_model: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    latency_ms: int
    error_message: str | None = None
