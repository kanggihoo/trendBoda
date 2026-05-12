from dataclasses import dataclass
from datetime import datetime

from trendboda.geeknews import StoredGeekNewsItem


@dataclass(frozen=True)
class GeekNewsSummary:
    item_id: int
    summary: str
    model: str
    generated_at: datetime


@dataclass(frozen=True)
class GeekNewsInsertResult:
    inserted_count: int
    inserted_items: list[StoredGeekNewsItem]
