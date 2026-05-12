from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request

from trendboda.ai import OpenRouterGateway, OpenRouterPricingCatalog
from trendboda.config import get_settings
from trendboda.geeknews import GeekNewsProvider
from trendboda.repositories import Repositories
from trendboda.services.geeknews import GeekNewsFetchService


def get_repositories(request: Request) -> Repositories:
    return request.app.state.container.repositories


def get_geeknews_provider(request: Request) -> GeekNewsProvider:
    return request.app.state.container.geeknews_provider


def get_geeknews_fetch_service(request: Request) -> GeekNewsFetchService:
    return request.app.state.container.geeknews_fetch_service


async def get_openrouter_gateway() -> AsyncGenerator[OpenRouterGateway]:
    settings = get_settings()
    if settings.openrouter_api_key is None:
        gateway = OpenRouterGateway(api_key="")
    else:
        gateway = OpenRouterGateway(api_key=settings.openrouter_api_key)
    try:
        yield gateway
    finally:
        await gateway.aclose()


async def get_pricing_catalog() -> AsyncGenerator[OpenRouterPricingCatalog]:
    catalog = OpenRouterPricingCatalog()
    try:
        yield catalog
    finally:
        await catalog.aclose()


RepositoriesDep = Annotated[Repositories, Depends(get_repositories)]
GeekNewsProviderDep = Annotated[GeekNewsProvider, Depends(get_geeknews_provider)]
GeekNewsFetchServiceDep = Annotated[GeekNewsFetchService, Depends(get_geeknews_fetch_service)]
OpenRouterGatewayDep = Annotated[OpenRouterGateway, Depends(get_openrouter_gateway)]
PricingCatalogDep = Annotated[OpenRouterPricingCatalog, Depends(get_pricing_catalog)]
