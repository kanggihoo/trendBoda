import pytest
from fastapi.testclient import TestClient

import trendboda.database as database
from trendboda.app import app


class FakePool:
    def __init__(self) -> None:
        self.closed = False

    async def close(self) -> None:
        self.closed = True


def test_app_lifespan_opens_and_closes_database_pool(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    created_pool = FakePool()

    async def fake_create_pool(database_url: str) -> FakePool:
        assert database_url == "postgres://user:pass@localhost:5432/testdb"
        return created_pool

    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@localhost:5432/testdb")
    monkeypatch.setattr(database, "create_pool", fake_create_pool)

    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert app.state.database_pool is created_pool

    assert created_pool.closed is True
