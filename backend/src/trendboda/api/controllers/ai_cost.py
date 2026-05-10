from typing import Annotated

from fastapi import APIRouter, Query

from trendboda.api.dependencies import RepositoriesDep
from trendboda.api.schemas import AICostSummaryResponse, AIUsageRequestsResponse
from trendboda.config import get_settings

router = APIRouter(prefix="/ai/cost")


@router.get("/summary")
async def get_ai_cost_summary(repositories: RepositoriesDep) -> AICostSummaryResponse:
    settings = get_settings()
    summary = await repositories.ai_usage.summarize_ai_cost(
        monthly_budget_usd=settings.ai_monthly_budget_usd
    )
    return AICostSummaryResponse.model_validate(summary)


@router.get("/requests")
async def list_ai_cost_requests(
    repositories: RepositoriesDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 25,
) -> AIUsageRequestsResponse:
    requests = await repositories.ai_usage.list_ai_usage_records(limit=limit)
    return AIUsageRequestsResponse.model_validate({"requests": requests})
