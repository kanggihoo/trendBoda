# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false

from typing import Protocol

import asyncpg


class DatabasePool(Protocol):
    async def close(self) -> None: ...


async def create_pool(database_url: str) -> asyncpg.Pool:
    return await asyncpg.create_pool(database_url)
