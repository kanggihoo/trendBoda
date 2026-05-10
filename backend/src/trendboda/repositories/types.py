from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class GeekNewsSummary:
    item_id: int
    summary: str
    model: str
    generated_at: datetime
