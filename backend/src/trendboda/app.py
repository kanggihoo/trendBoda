from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel, ConfigDict

from trendboda import database
from trendboda.config import get_settings
from trendboda.geeknews import GeekNewsProvider
from trendboda.repositories import Repositories


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    settings = get_settings()
    pool = await database.create_pool(settings.database_url)
    app.state.database_pool = pool
    app.state.repositories = Repositories(pool=pool)
    try:
        yield
    finally:
        await pool.close()


app = FastAPI(title="TrendBoda API", lifespan=lifespan)


class GeekNewsItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str
    title: str
    source_url: str
    published_at: str | None
    fetched_at: str


class GeekNewsItemsResponse(BaseModel):
    items: list[GeekNewsItemResponse]


class GeekNewsFetchResponse(BaseModel):
    fetch_run_id: int
    fetched_count: int
    inserted_count: int


def get_repositories() -> Repositories:
    return app.state.repositories


def get_geeknews_provider() -> GeekNewsProvider:
    return GeekNewsProvider()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "trendboda-api"}


@app.get("/geeknews/items")
async def list_geeknews_items(
    repositories: Annotated[Repositories, Depends(get_repositories)],
) -> GeekNewsItemsResponse:
    items = await repositories.geeknews.list_recent_items(limit=50)
    return GeekNewsItemsResponse(
        items=[
            GeekNewsItemResponse(
                id=item.id,
                external_id=item.external_id,
                title=item.title,
                source_url=item.source_url,
                published_at=item.published_at.isoformat() if item.published_at else None,
                fetched_at=item.fetched_at.isoformat(),
            )
            for item in items
        ]
    )


@app.post("/geeknews/fetch")
async def fetch_geeknews(
    repositories: Annotated[Repositories, Depends(get_repositories)],
    provider: Annotated[GeekNewsProvider, Depends(get_geeknews_provider)],
) -> GeekNewsFetchResponse:
    items = await provider.fetch_items()
    fetch_run_id = await repositories.geeknews.record_fetch_run(
        status="success",
        item_count=len(items),
    )
    inserted_count = await repositories.geeknews.upsert_items(
        fetch_run_id=fetch_run_id, items=items
    )
    return GeekNewsFetchResponse(
        fetch_run_id=fetch_run_id,
        fetched_count=len(items),
        inserted_count=inserted_count,
    )
