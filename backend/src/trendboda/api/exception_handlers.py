import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from trendboda.api.middleware import REQUEST_ID_HEADER, get_request_id
from trendboda.exceptions import TrendBodaError

logger = logging.getLogger("trendboda.api")

HTTP_ERROR_MESSAGES = {
    400: ("bad_request", "Bad request"),
    401: ("unauthorized", "Unauthorized"),
    403: ("forbidden", "Forbidden"),
    404: ("not_found", "Not found"),
    405: ("method_not_allowed", "Method not allowed"),
    409: ("conflict", "Conflict"),
    422: ("validation_failed", "Request validation failed"),
    429: ("rate_limited", "Rate limited"),
    500: ("internal_server_error", "Internal server error"),
    502: ("bad_gateway", "Bad gateway"),
}


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(TrendBodaError, handle_app_error)
    app.add_exception_handler(StarletteHTTPException, handle_http_error)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(Exception, handle_unexpected_error)


async def handle_app_error(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, TrendBodaError):
        raise exc

    request_id = get_request_id(request)
    logger.warning(
        "api_error",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": exc.status_code,
            "error_code": exc.code,
        },
    )
    return _error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.public_message,
        request_id=request_id,
    )


async def handle_http_error(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, StarletteHTTPException):
        raise exc

    request_id = get_request_id(request)
    code, message = HTTP_ERROR_MESSAGES.get(exc.status_code, ("http_error", "Request failed"))
    logger.warning(
        "api_error",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": exc.status_code,
            "error_code": code,
        },
    )
    return _error_response(
        status_code=exc.status_code,
        code=code,
        message=message,
        request_id=request_id,
    )


async def handle_validation_error(request: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        raise exc

    request_id = get_request_id(request)
    logger.warning(
        "api_error",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": 422,
            "error_code": "validation_failed",
            "validation_errors": exc.errors(),
        },
    )
    return _error_response(
        status_code=422,
        code="validation_failed",
        message="Request validation failed",
        request_id=request_id,
    )


async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    request_id = get_request_id(request)
    logger.exception(
        "api_unhandled_exception",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": 500,
            "error_code": "internal_server_error",
        },
    )
    return _error_response(
        status_code=500,
        code="internal_server_error",
        message="Internal server error",
        request_id=request_id,
    )


def _error_response(*, status_code: int, code: str, message: str, request_id: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": request_id,
            }
        },
        headers={REQUEST_ID_HEADER: request_id},
    )
