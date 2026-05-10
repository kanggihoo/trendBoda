from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request

from trendboda.ai import OpenRouterGateway, OpenRouterPricingCatalog
from trendboda.config import get_settings
from trendboda.geeknews import GeekNewsProvider
from trendboda.repositories import Repositories


def get_repositories(request: Request) -> Repositories:
    return request.app.state.repositories


def get_geeknews_provider() -> GeekNewsProvider:
    return GeekNewsProvider()


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
OpenRouterGatewayDep = Annotated[OpenRouterGateway, Depends(get_openrouter_gateway)]
PricingCatalogDep = Annotated[OpenRouterPricingCatalog, Depends(get_pricing_catalog)]
