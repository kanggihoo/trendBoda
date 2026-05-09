from trendboda.repositories import Repositories


class FakePool:
    pass


def test_repositories_expose_shared_database_pool() -> None:
    pool = FakePool()

    repositories = Repositories(pool=pool)

    assert repositories.pool is pool
