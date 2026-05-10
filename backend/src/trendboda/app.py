from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from trendboda import database
from trendboda.api.controllers.ai_cost import router as ai_cost_router
from trendboda.api.controllers.geeknews import router as geeknews_router
from trendboda.api.controllers.health import router as health_router
from trendboda.api.exception_handlers import register_exception_handlers
from trendboda.api.middleware import RequestIdMiddleware
from trendboda.config import get_settings
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
app.add_middleware(RequestIdMiddleware)
register_exception_handlers(app)
app.include_router(health_router)
app.include_router(geeknews_router)
app.include_router(ai_cost_router)
