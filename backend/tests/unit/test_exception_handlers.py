import logging

from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

from trendboda.api.exception_handlers import register_exception_handlers
from trendboda.api.middleware import RequestIdMiddleware
from trendboda.exceptions import GeekNewsFetchFailed


def create_test_app() -> FastAPI:
    test_app = FastAPI()
    test_app.add_middleware(RequestIdMiddleware)
    register_exception_handlers(test_app)
    return test_app


def test_app_exception_handler_returns_existing_detail_shape(caplog) -> None:  # type: ignore[no-untyped-def]
    test_app = create_test_app()

    @test_app.get("/boom")
    async def boom() -> None:
        raise GeekNewsFetchFailed()

    with caplog.at_level(logging.WARNING, logger="trendboda.api"):
        response = TestClient(test_app, raise_server_exceptions=False).get("/boom")

    assert response.status_code == 502
    assert response.json() == {
        "error": {
            "code": "geeknews_fetch_failed",
            "message": "GeekNews fetch failed",
            "request_id": response.headers["x-request-id"],
        }
    }
    assert any(record.error_code == "geeknews_fetch_failed" for record in caplog.records)
    assert any(record.request_id == response.headers["x-request-id"] for record in caplog.records)


def test_unexpected_exception_handler_returns_internal_server_error(caplog) -> None:  # type: ignore[no-untyped-def]
    test_app = create_test_app()

    @test_app.get("/boom")
    async def boom() -> None:
        raise RuntimeError("database password leaked")

    with caplog.at_level(logging.ERROR, logger="trendboda.api"):
        response = TestClient(test_app, raise_server_exceptions=False).get("/boom")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "internal_server_error",
            "message": "Internal server error",
            "request_id": response.headers["x-request-id"],
        }
    }
    assert "database password leaked" not in response.text
    assert any(record.exc_info for record in caplog.records)


def test_request_id_middleware_reuses_valid_inbound_request_id() -> None:
    test_app = create_test_app()

    @test_app.get("/ok")
    async def ok() -> dict[str, str]:
        return {"status": "ok"}

    response = TestClient(test_app).get("/ok", headers={"X-Request-ID": "req_client-123"})

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req_client-123"
    assert response.json() == {"status": "ok"}


def test_request_id_middleware_replaces_invalid_inbound_request_id() -> None:
    test_app = create_test_app()

    @test_app.get("/ok")
    async def ok() -> dict[str, str]:
        return {"status": "ok"}

    response = TestClient(test_app).get("/ok", headers={"X-Request-ID": "bad request id"})

    assert response.status_code == 200
    assert response.headers["x-request-id"].startswith("req_")
    assert response.headers["x-request-id"] != "bad request id"


def test_http_exception_handler_returns_standard_error_shape() -> None:
    response = TestClient(create_test_app()).get("/missing")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "not_found",
            "message": "Not found",
            "request_id": response.headers["x-request-id"],
        }
    }


def test_validation_exception_handler_returns_standard_error_shape(caplog) -> None:  # type: ignore[no-untyped-def]
    test_app = create_test_app()

    @test_app.get("/items")
    async def items(limit: int = Query(le=50)) -> dict[str, int]:
        return {"limit": limit}

    with caplog.at_level(logging.WARNING, logger="trendboda.api"):
        response = TestClient(test_app).get("/items?limit=99")

    assert response.status_code == 422
    assert response.json() == {
        "error": {
            "code": "validation_failed",
            "message": "Request validation failed",
            "request_id": response.headers["x-request-id"],
        }
    }
    assert "less_than_equal" not in response.text
    assert any(record.error_code == "validation_failed" for record in caplog.records)
    assert any(hasattr(record, "validation_errors") for record in caplog.records)


def test_request_completion_is_logged(caplog) -> None:  # type: ignore[no-untyped-def]
    test_app = create_test_app()

    @test_app.get("/ok")
    async def ok() -> dict[str, str]:
        return {"status": "ok"}

    with caplog.at_level(logging.INFO, logger="trendboda.api"):
        response = TestClient(test_app).get("/ok")

    assert response.status_code == 200
    assert any(
        record.message == "request_completed"
        and record.request_id == response.headers["x-request-id"]
        and record.status_code == 200
        and hasattr(record, "duration_ms")
        for record in caplog.records
    )
