from pydantic import BaseModel, ConfigDict


class GeekNewsItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str
    title: str
    source_url: str
    content_text: str
    published_at: str | None
    fetched_at: str
    summary: "GeekNewsSummaryResponse | None" = None


class GeekNewsItemsResponse(BaseModel):
    items: list[GeekNewsItemResponse]


class GeekNewsFetchResponse(BaseModel):
    fetch_run_id: int
    fetched_count: int
    inserted_count: int


class GeekNewsSummaryResponse(BaseModel):
    item_id: int
    summary: str
    model: str
    generated_at: str
