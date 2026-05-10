from decimal import Decimal

import httpx
import pytest
import respx

from trendboda.ai import (
    AIFeature,
    AIModel,
    AIUsageStatus,
    OpenRouterGateway,
    OpenRouterModelPricing,
    OpenRouterPricingCatalog,
    calculate_estimated_cost_usd,
    default_ai_routes,
)


def test_geeknews_summary_route_uses_primary_and_fallback_models() -> None:
    routes = default_ai_routes()

    route = routes[AIFeature.GEEKNEWS_SUMMARY]

    assert route.models == [
        AIModel.OPENAI_GPT_4_1_NANO,
        AIModel.GOOGLE_GEMINI_2_5_FLASH_LITE,
    ]
    assert route.openrouter_models == [
        "openai/gpt-4.1-nano",
        "google/gemini-2.5-flash-lite",
    ]


def test_cost_uses_prompt_and_completion_pricing_snapshot() -> None:
    cost = calculate_estimated_cost_usd(
        prompt_tokens=1000,
        completion_tokens=2000,
        pricing=OpenRouterModelPricing(
            prompt_per_million=Decimal("0.10"),
            completion_per_million=Decimal("0.40"),
            source="openrouter",
            raw={"prompt": "0.10", "completion": "0.40"},
        ),
    )

    assert cost == Decimal("0.000900")


def test_cost_is_unavailable_when_usage_or_pricing_missing() -> None:
    assert calculate_estimated_cost_usd(
        prompt_tokens=None,
        completion_tokens=10,
        pricing=OpenRouterModelPricing(
            prompt_per_million=Decimal("0.10"),
            completion_per_million=Decimal("0.40"),
            source="fallback",
            raw={},
        ),
    ) is None
    assert calculate_estimated_cost_usd(prompt_tokens=0, completion_tokens=0, pricing=None) is None


@respx.mock
@pytest.mark.asyncio
async def test_openrouter_gateway_normalizes_success_with_usage_latency_and_actual_model() -> None:
    respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "model": "google/gemini-2.5-flash-lite",
                "choices": [{"message": {"content": "Short summary"}}],
                "usage": {"prompt_tokens": 12, "completion_tokens": 5, "total_tokens": 17},
            },
        )
    )
    gateway = OpenRouterGateway(api_key="test-key", http_client=httpx.AsyncClient())

    try:
        result = await gateway.complete(
            models=["openai/gpt-4.1-nano", "google/gemini-2.5-flash-lite"],
            messages=[{"role": "user", "content": "Summarize"}],
        )
    finally:
        await gateway.aclose()

    assert result.status == AIUsageStatus.SUCCESS
    assert result.content == "Short summary"
    assert result.actual_model == "google/gemini-2.5-flash-lite"
    assert result.prompt_tokens == 12
    assert result.completion_tokens == 5
    assert result.total_tokens == 17
    assert result.latency_ms >= 0


@respx.mock
@pytest.mark.asyncio
async def test_openrouter_gateway_normalizes_failure() -> None:
    respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=httpx.Response(429, json={"error": {"message": "rate limited"}})
    )
    gateway = OpenRouterGateway(api_key="test-key", http_client=httpx.AsyncClient())

    try:
        result = await gateway.complete(
            models=["openai/gpt-4.1-nano"],
            messages=[{"role": "user", "content": "Summarize"}],
        )
    finally:
        await gateway.aclose()

    assert result.status == AIUsageStatus.FAILURE
    assert result.content is None
    assert result.error_message == "rate limited"
    assert result.latency_ms >= 0


@respx.mock
@pytest.mark.asyncio
async def test_pricing_catalog_reads_openrouter_models_metadata() -> None:
    respx.get("https://openrouter.ai/api/v1/models").mock(
        return_value=httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "openai/gpt-4.1-nano",
                        "pricing": {"prompt": "0.0000001", "completion": "0.0000004"},
                    }
                ]
            },
        )
    )
    catalog = OpenRouterPricingCatalog(http_client=httpx.AsyncClient())

    try:
        pricing = await catalog.get_pricing("openai/gpt-4.1-nano")
    finally:
        await catalog.aclose()

    assert pricing == OpenRouterModelPricing(
        prompt_per_million=Decimal("0.1000000"),
        completion_per_million=Decimal("0.4000000"),
        source="openrouter",
        raw={"prompt": "0.0000001", "completion": "0.0000004"},
    )
