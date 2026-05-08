# Local development runs apps on host with Dockerized Postgres

TrendBoda local development will run Postgres through Docker Compose while FastAPI and Next.js run directly on the developer machine. We chose this because host-run app processes give faster hot reload and simpler debugging, while Dockerized Postgres keeps the database environment reproducible.

## Consequences

- Local setup starts the database with Docker Compose, then runs API and web processes separately.
- Deployment can still use Docker Compose for backend services and Caddy on EC2.
- Local and deployed process topology may differ, so health checks and configuration must stay environment-aware.
