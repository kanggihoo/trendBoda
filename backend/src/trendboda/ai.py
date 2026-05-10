from __future__ import annotations

import time
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum
from typing import Any, cast

import httpx

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class AIFeature(StrEnum):
    GEEKNEWS_SUMMARY = "geeknews_summary"


class AIModel(StrEnum):
    OPENAI_GPT_4_1_NANO = "openai_gpt_4_1_nano"
    GOOGLE_GEMINI_2_5_FLASH_LITE = "google_gemini_2_5_flash_lite"


class AIUsageStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"


OPENROUTER_MODEL_IDS: dict[AIModel, str] = {
    AIModel.OPENAI_GPT_4_1_NANO: "openai/gpt-4.1-nano",
    AIModel.GOOGLE_GEMINI_2_5_FLASH_LITE: "google/gemini-2.5-flash-lite",
}


@dataclass(frozen=True)
class AIRoute:
    feature: AIFeature
    models: list[AIModel]

    @property
    def openrouter_models(self) -> list[str]:
        return [OPENROUTER_MODEL_IDS[model] for model in self.models]


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


def default_ai_routes() -> dict[AIFeature, AIRoute]:
    return {
        AIFeature.GEEKNEWS_SUMMARY: AIRoute(
            feature=AIFeature.GEEKNEWS_SUMMARY,
            models=[
                AIModel.OPENAI_GPT_4_1_NANO,
                AIModel.GOOGLE_GEMINI_2_5_FLASH_LITE,
            ],
        )
    }


def calculate_estimated_cost_usd(
    *,
    prompt_tokens: int | None,
    completion_tokens: int | None,
    pricing: OpenRouterModelPricing | None,
) -> Decimal | None:
    if prompt_tokens is None or completion_tokens is None or pricing is None:
        return None

    prompt_cost = Decimal(prompt_tokens) * pricing.prompt_per_million / Decimal(1_000_000)
    completion_cost = (
        Decimal(completion_tokens) * pricing.completion_per_million / Decimal(1_000_000)
    )
    return prompt_cost + completion_cost


class OpenRouterGateway:
    def __init__(
        self,
        *,
        api_key: str,
        http_client: httpx.AsyncClient | None = None,
        base_url: str = OPENROUTER_BASE_URL,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(timeout=30.0)

    async def complete(
        self,
        *,
        models: list[str],
        messages: list[dict[str, str]],
    ) -> OpenRouterResult:
        started = time.perf_counter()
        try:
            response = await self._client.post(
                f"{self._base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={"models": models, "messages": messages},
            )
        except httpx.HTTPError as exc:
            return OpenRouterResult(
                status=AIUsageStatus.FAILURE,
                content=None,
                actual_model=None,
                prompt_tokens=None,
                completion_tokens=None,
                total_tokens=None,
                latency_ms=_latency_ms(started),
                error_message=str(exc),
            )

        payload = _json_object(response)
        if response.is_error:
            return OpenRouterResult(
                status=AIUsageStatus.FAILURE,
                content=None,
                actual_model=_optional_str(payload.get("model")),
                prompt_tokens=None,
                completion_tokens=None,
                total_tokens=None,
                latency_ms=_latency_ms(started),
                error_message=_error_message(payload, response),
            )

        usage = _mapping(payload.get("usage"))
        return OpenRouterResult(
            status=AIUsageStatus.SUCCESS,
            content=_content(payload),
            actual_model=_optional_str(payload.get("model")),
            prompt_tokens=_optional_int(usage.get("prompt_tokens")),
            completion_tokens=_optional_int(usage.get("completion_tokens")),
            total_tokens=_optional_int(usage.get("total_tokens")),
            latency_ms=_latency_ms(started),
        )

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()


class OpenRouterPricingCatalog:
    def __init__(
        self,
        *,
        http_client: httpx.AsyncClient | None = None,
        base_url: str = OPENROUTER_BASE_URL,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(timeout=10.0)
        self._cache: dict[str, OpenRouterModelPricing] | None = None
        self._cached_at = 0.0

    async def get_pricing(self, model: str) -> OpenRouterModelPricing | None:
        prices = await self._prices()
        return prices.get(model) or _fallback_pricing(model)

    async def _prices(self) -> dict[str, OpenRouterModelPricing]:
        now = time.monotonic()
        if self._cache is not None and now - self._cached_at < 86_400:
            return self._cache

        try:
            response = await self._client.get(f"{self._base_url}/models")
            response.raise_for_status()
        except httpx.HTTPError:
            self._cache = {}
            self._cached_at = now
            return {}

        payload = _json_object(response)
        prices: dict[str, OpenRouterModelPricing] = {}
        data = payload.get("data")
        if isinstance(data, list):
            for item in cast(list[object], data):
                if not isinstance(item, Mapping):
                    continue
                model_id = _optional_str(cast(Mapping[str, object], item).get("id"))
                pricing = _mapping(cast(Mapping[str, object], item).get("pricing"))
                if model_id is None:
                    continue
                parsed = _parse_pricing(pricing, source="openrouter")
                if parsed is not None:
                    prices[model_id] = parsed

        self._cache = prices
        self._cached_at = now
        return prices

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()


def _parse_pricing(
    pricing: Mapping[str, object],
    *,
    source: str,
) -> OpenRouterModelPricing | None:
    prompt = _decimal_or_none(pricing.get("prompt"))
    completion = _decimal_or_none(pricing.get("completion"))
    if prompt is None or completion is None:
        return None
    return OpenRouterModelPricing(
        prompt_per_million=prompt * Decimal(1_000_000),
        completion_per_million=completion * Decimal(1_000_000),
        source=source,
        raw=dict(pricing),
    )


def _fallback_pricing(model: str) -> OpenRouterModelPricing | None:
    fallback_by_model = {
        "openai/gpt-4.1-nano": {"prompt": "0.00000010", "completion": "0.00000040"},
        "google/gemini-2.5-flash-lite": {
            "prompt": "0.00000010",
            "completion": "0.00000040",
        },
    }
    pricing = fallback_by_model.get(model)
    if pricing is None:
        return None
    return _parse_pricing(pricing, source="fallback")


def _json_object(response: httpx.Response) -> dict[str, object]:
    try:
        payload: object = response.json()
    except ValueError:
        return {}
    if isinstance(payload, dict):
        return cast(dict[str, object], payload)
    return {}


def _content(payload: Mapping[str, object]) -> str | None:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    choice = cast(list[object], choices)[0]
    if not isinstance(choice, Mapping):
        return None
    message = cast(Mapping[str, object], choice).get("message")
    if not isinstance(message, Mapping):
        return None
    return _optional_str(cast(Mapping[str, object], message).get("content"))


def _error_message(payload: Mapping[str, object], response: httpx.Response) -> str:
    error = payload.get("error")
    if isinstance(error, Mapping):
        message = _optional_str(cast(Mapping[str, object], error).get("message"))
        if message:
            return message
    return f"OpenRouter returned {response.status_code}"


def _mapping(value: object) -> Mapping[str, object]:
    if isinstance(value, Mapping):
        return cast(Mapping[str, object], value)
    return {}


def _optional_str(value: object) -> str | None:
    if isinstance(value, str):
        return value
    return None


def _optional_int(value: object) -> int | None:
    if isinstance(value, int):
        return value
    return None


def _decimal_or_none(value: object) -> Decimal | None:
    if isinstance(value, str | int | float):
        return Decimal(str(value))
    return None


def _latency_ms(started: float) -> int:
    return int((time.perf_counter() - started) * 1000)
