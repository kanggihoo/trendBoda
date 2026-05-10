from decimal import Decimal

from trendboda.ai.types import OpenRouterModelPricing


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
