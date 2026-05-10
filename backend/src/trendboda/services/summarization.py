from dataclasses import dataclass

from trendboda.ai import (
    AIFeature,
    AIUsageStatus,
    OpenRouterGateway,
    OpenRouterPricingCatalog,
    calculate_estimated_cost_usd,
    default_ai_routes,
)
from trendboda.exceptions import GeekNewsItemNotFound, GeekNewsSummaryFailed
from trendboda.repositories import GeekNewsRepository, GeekNewsSummary


@dataclass(frozen=True)
class GeekNewsSummaryService:
    repository: GeekNewsRepository
    gateway: OpenRouterGateway
    pricing_catalog: OpenRouterPricingCatalog

    async def generate(self, *, item_id: int) -> GeekNewsSummary:
        item = await self.repository.get_item(item_id=item_id)
        if item is None:
            raise GeekNewsItemNotFound

        route = default_ai_routes()[AIFeature.GEEKNEWS_SUMMARY]
        requested_models = route.openrouter_models
        result = await self.gateway.complete(
            models=requested_models,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Summarize Developer Trend Source signals for the TrendBoda Owner. "
                        "Return concise Korean summary with practical relevance."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Title: {item.title}\nURL: {item.source_url}",
                },
            ],
        )
        pricing = None
        if result.actual_model is not None:
            pricing = await self.pricing_catalog.get_pricing(result.actual_model)
        estimated_cost = calculate_estimated_cost_usd(
            prompt_tokens=result.prompt_tokens,
            completion_tokens=result.completion_tokens,
            pricing=pricing,
        )
        await self.repository.record_ai_usage(
            feature=AIFeature.GEEKNEWS_SUMMARY,
            status=result.status,
            requested_models=requested_models,
            actual_model=result.actual_model,
            prompt_tokens=result.prompt_tokens,
            completion_tokens=result.completion_tokens,
            total_tokens=result.total_tokens,
            estimated_cost_usd=estimated_cost,
            latency_ms=result.latency_ms,
            pricing_source=pricing.source if pricing is not None else None,
            pricing_snapshot=pricing.raw if pricing is not None else None,
            error_message=result.error_message,
        )
        if result.status != AIUsageStatus.SUCCESS or not result.content or not result.actual_model:
            raise GeekNewsSummaryFailed

        return await self.repository.upsert_summary(
            item_id=item.id,
            summary=result.content,
            model=result.actual_model,
        )
