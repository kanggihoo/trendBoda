from typing import Annotated

from fastapi import Depends, Request

from trendboda.geeknews import GeekNewsProvider
from trendboda.repositories import Repositories


def get_repositories(request: Request) -> Repositories:
    return request.app.state.repositories


def get_geeknews_provider() -> GeekNewsProvider:
    return GeekNewsProvider()


RepositoriesDep = Annotated[Repositories, Depends(get_repositories)]
GeekNewsProviderDep = Annotated[GeekNewsProvider, Depends(get_geeknews_provider)]
