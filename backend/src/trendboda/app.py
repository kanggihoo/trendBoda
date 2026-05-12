from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from trendboda.api.controllers.ai_cost import router as ai_cost_router
from trendboda.api.controllers.geeknews import router as geeknews_router
from trendboda.api.controllers.health import router as health_router
from trendboda.api.exception_handlers import register_exception_handlers
from trendboda.api.middleware import RequestIdMiddleware
from trendboda.bootstrap import bootstrap_application


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    async with bootstrap_application() as container:
        app.state.container = container
        app.state.database_pool = container.pool
        app.state.repositories = container.repositories
        yield


app = FastAPI(title="TrendBoda API", lifespan=lifespan)
app.add_middleware(RequestIdMiddleware)
register_exception_handlers(app)
app.include_router(health_router)
app.include_router(geeknews_router)
app.include_router(ai_cost_router)
