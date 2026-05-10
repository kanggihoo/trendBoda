import time
from collections.abc import Mapping
from decimal import Decimal
from typing import cast

import httpx

from trendboda.ai.json import decimal_or_none, json_object, mapping, optional_str
from trendboda.ai.types import OPENROUTER_BASE_URL, OpenRouterModelPricing


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

        payload = json_object(response)
        prices: dict[str, OpenRouterModelPricing] = {}
        data = payload.get("data")
        if isinstance(data, list):
            for item in cast(list[object], data):
                if not isinstance(item, Mapping):
                    continue
                model_id = optional_str(cast(Mapping[str, object], item).get("id"))
                pricing = mapping(cast(Mapping[str, object], item).get("pricing"))
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
    prompt = decimal_or_none(pricing.get("prompt"))
    completion = decimal_or_none(pricing.get("completion"))
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
