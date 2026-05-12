from fastapi import APIRouter

from trendboda.api.dependencies import (
    GeekNewsProviderDep,
    RepositoriesDep,
)
from trendboda.api.schemas import (
    GeekNewsFetchResponse,
    GeekNewsItemResponse,
    GeekNewsItemsResponse,
)
from trendboda.services.geeknews import GeekNewsFetchService

router = APIRouter(prefix="/geeknews")


# TODO : limit도 파라미터로?
@router.get("/items")
async def list_geeknews_items(
    repositories: RepositoriesDep,
) -> GeekNewsItemsResponse:
    items = await repositories.geeknews.list_recent_items(limit=50)
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
