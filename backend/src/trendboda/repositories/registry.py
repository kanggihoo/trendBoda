from dataclasses import dataclass
from typing import Any

from trendboda.repositories.ai_usage import AIUsageRepository
from trendboda.repositories.geeknews import GeekNewsRepository


@dataclass(frozen=True)
class Repositories:
    pool: Any

    @property
    def geeknews(self) -> GeekNewsRepository:
        return GeekNewsRepository(self.pool)

    @property
    def ai_usage(self) -> AIUsageRepository:
        return AIUsageRepository(self.pool)
