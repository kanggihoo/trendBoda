from collections.abc import Iterator
from pathlib import Path
from subprocess import run

import pytest
from testcontainers.postgres import PostgresContainer

ROOT_DIR = Path(__file__).resolve().parents[3]


@pytest.fixture(scope="session")
def migrated_database_url() -> Iterator[str]:
    with PostgresContainer("postgres:16-alpine") as postgres:
        database_url = _asyncpg_url(postgres)
        run(
            [
                "dbmate",
                "--url",
                database_url,
                "--migrations-dir",
                str(ROOT_DIR / "db" / "migrations"),
                "--no-dump-schema",
                "up",
            ],
            check=True,
            cwd=ROOT_DIR,
        )
        yield database_url


def _asyncpg_url(postgres: PostgresContainer) -> str:
    return (
        "postgres://"
        f"{postgres.username}:{postgres.password}"
        f"@{postgres.get_container_host_ip()}:{postgres.get_exposed_port(5432)}"
        f"/{postgres.dbname}?sslmode=disable"
    )
