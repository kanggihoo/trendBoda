from pydantic import BaseModel


class AICostTotalsResponse(BaseModel):
    estimated_cost_usd: str
    request_count: int
    success_count: int
    failure_count: int
    average_latency_ms: int | None


class AICostGroupBaseResponse(BaseModel):
    estimated_cost_usd: str
    request_count: int
    average_latency_ms: int | None
    failure_count: int


class AICostDateGroupResponse(AICostGroupBaseResponse):
    date: str


class AICostModelGroupResponse(AICostGroupBaseResponse):
    model: str


class AICostFeatureGroupResponse(AICostGroupBaseResponse):
    feature: str


class AICostBudgetResponse(BaseModel):
    monthly_budget_usd: str
    estimated_monthly_cost_usd: str
    percent_used: str


class AICostSummaryResponse(BaseModel):
    totals: AICostTotalsResponse
    by_date: list[AICostDateGroupResponse]
    by_model: list[AICostModelGroupResponse]
    by_feature: list[AICostFeatureGroupResponse]
    budget: AICostBudgetResponse


class AIUsageRequestResponse(BaseModel):
    id: int
    feature: str
    status: str
    requested_models: list[str]
    actual_model: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    estimated_cost_usd: str
    latency_ms: int
    pricing_source: str | None
    error_message: str | None
    created_at: str


class AIUsageRequestsResponse(BaseModel):
    requests: list[AIUsageRequestResponse]
