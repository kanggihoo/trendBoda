from collections.abc import Mapping
from dataclasses import dataclass
from typing import Protocol

from trendboda.geeknews import StoredGeekNewsItem


@dataclass(frozen=True)
class GeekNewsTelegramItem:
    title: str
    source_url: str
    content_text: str


class TelegramGeekNewsRepository(Protocol):
    async def list_recent_items(self, *, limit: int) -> list[StoredGeekNewsItem]: ...


class TelegramAIUsageRepository(Protocol):
    async def summarize_ai_cost(self, *, monthly_budget_usd: str) -> dict[str, object]: ...


class TelegramRepositories(Protocol):
    @property
    def geeknews(self) -> TelegramGeekNewsRepository: ...

    @property
    def ai_usage(self) -> TelegramAIUsageRepository: ...


TelegramUpdate = Mapping[str, object]
TelegramOutgoingPayload = dict[str, object]
