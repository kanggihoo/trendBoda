# FastAPI with asyncpg repositories and dbmate migrations

TrendBoda backend will use FastAPI with asyncpg for PostgreSQL access, repository classes as the Python-to-database boundary, uv for Python dependency and command management, and dbmate for SQL migrations. We chose this to keep the backend in Python for market-data workflows while avoiding SQLAlchemy and keeping database schema changes explicit, lightweight, and versioned.

## Consequences

- Application code must not build ad hoc database queries outside repositories.
- Services own transaction boundaries when a workflow spans multiple repository calls.
- Python dependencies and backend commands are managed through uv.
- Migrations are written as SQL files with dbmate `migrate:up` and `migrate:down` sections.
