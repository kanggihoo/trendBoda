from fastapi import APIRouter

from trendboda.api.dependencies import (
    GeekNewsProviderDep,
    OpenRouterGatewayDep,
    PricingCatalogDep,
    RepositoriesDep,
)
from trendboda.api.schemas import (
    GeekNewsFetchResponse,
    GeekNewsItemResponse,
    GeekNewsItemsResponse,
    GeekNewsSummaryResponse,
)
from trendboda.exceptions import GeekNewsItemNotFound
from trendboda.repositories import GeekNewsSummary
from trendboda.services.geeknews import GeekNewsFetchService
from trendboda.services.summarization import GeekNewsSummaryService

router = APIRouter(prefix="/geeknews")


# TODO : limit도 파라미터로?
@router.get("/items")
async def list_geeknews_items(
    repositories: RepositoriesDep,
) -> GeekNewsItemsResponse:
    items = await repositories.geeknews.list_recent_items(limit=50)
    summaries = {
        item.id: await repositories.geeknews.get_summary(item_id=item.id) for item in items
    }
    return GeekNewsItemsResponse(
        items=[
            GeekNewsItemResponse(
                id=item.id,
                external_id=item.external_id,
                title=item.title,
                source_url=item.source_url,
                content_text=item.content_text,
                published_at=item.published_at.isoformat() if item.published_at else None,
                fetched_at=item.fetched_at.isoformat(),
                summary=_summary_response(summaries[item.id]),
            )
            for item in items
        ]
    )


@router.post("/fetch-runs")
@router.post("/fetch", deprecated=True)
async def fetch_geeknews(
    repositories: RepositoriesDep,
    provider: GeekNewsProviderDep,
) -> GeekNewsFetchResponse:
    result = await GeekNewsFetchService(
        repository=repositories.geeknews,
        provider=provider,
    ).fetch()
    return GeekNewsFetchResponse(
        fetch_run_id=result.fetch_run_id,
        fetched_count=result.fetched_count,
        inserted_count=result.inserted_count,
    )


@router.get("/items/{item_id}/summary")
async def get_geeknews_summary(
    item_id: int,
    repositories: RepositoriesDep,
) -> GeekNewsSummaryResponse:
    summary = await repositories.geeknews.get_summary(item_id=item_id)
    if summary is None:
        raise GeekNewsItemNotFound
    return _required_summary_response(summary)


@router.post("/items/{item_id}/summary-runs")
@router.post("/items/{item_id}/summary", deprecated=True)
async def generate_geeknews_summary(
    item_id: int,
    repositories: RepositoriesDep,
    gateway: OpenRouterGatewayDep,
    pricing_catalog: PricingCatalogDep,
) -> GeekNewsSummaryResponse:
    summary = await GeekNewsSummaryService(
        repository=repositories.geeknews,
        ai_usage_repository=repositories.ai_usage,
        gateway=gateway,
        pricing_catalog=pricing_catalog,
    ).generate(item_id=item_id)
    return _required_summary_response(summary)


def _summary_response(summary: GeekNewsSummary | None) -> GeekNewsSummaryResponse | None:
    if summary is None:
        return None
    return _required_summary_response(summary)


def _required_summary_response(summary: GeekNewsSummary) -> GeekNewsSummaryResponse:
    return GeekNewsSummaryResponse(
        item_id=summary.item_id,
        summary=summary.summary,
        model=summary.model,
        generated_at=summary.generated_at.isoformat(),
    )
