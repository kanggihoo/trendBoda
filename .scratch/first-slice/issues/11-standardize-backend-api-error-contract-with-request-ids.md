Status: done
Type: AFK

# Standardize backend API error contract with request IDs

## Parent

.scratch/first-slice/PRD.md

## What to build

Introduce a backend-only API error response contract for FastAPI errors, with request IDs that connect client-visible failures to backend logs. Keep successful response bodies unchanged. Standardize app exceptions, HTTP exceptions, validation errors, and unexpected exceptions into one public error shape.

This issue intentionally changes error response bodies and should be implemented after the service/global-handler refactor in issue 10. Do not update the web dashboard client in this issue unless a no-op compatibility check is required.

## User stories covered

- 25. Expose health checks
- 26. Expose GeekNews item APIs
- 27. Expose summary APIs
- 28. Expose AI cost APIs
- 39. Test parser, storage, API contracts, dashboard behavior, and Telegram formatting

## Error response contract

All backend API errors should return this shape:

```json
{
  "error": {
    "code": "validation_failed",
    "message": "Request validation failed",
    "request_id": "req_..."
  }
}
```

The public response must not include validation field details, stack traces, provider raw errors, database raw errors, request headers, request body, or secrets. Detailed debugging information belongs in backend logs only.

## Error code mapping

- App exceptions use their app-level `code`, `status_code`, and fixed public message.
- `400` maps to `bad_request` and `Bad request`.
- `401` maps to `unauthorized` and `Unauthorized`.
- `403` maps to `forbidden` and `Forbidden`.
- `404` maps to `not_found` and `Not found`.
- `405` maps to `method_not_allowed` and `Method not allowed`.
- `409` maps to `conflict` and `Conflict`.
- `422` maps to `validation_failed` and `Request validation failed`.
- `429` maps to `rate_limited` and `Rate limited`.
- `500` maps to `internal_server_error` and `Internal server error`.
- `502` maps to `bad_gateway` and `Bad gateway`.
- Unknown HTTP statuses map to `http_error` and `Request failed`.

## Acceptance criteria

- [x] `RequestIdMiddleware` is created and registered for the FastAPI app.
- [x] Inbound `X-Request-ID` is reused only when it passes validation.
- [x] Missing or invalid inbound `X-Request-ID` values are replaced by a generated `req_<uuid>` value.
- [x] Every response includes an `X-Request-ID` header.
- [x] Error response bodies include the same `request_id` value as the response header.
- [x] App exceptions return `{ "error": { "code", "message", "request_id" } }`.
- [x] FastAPI/Starlette HTTP exceptions, including 404 and 405, return the standard error shape.
- [x] Request validation errors return the standard error shape with `validation_failed`.
- [x] Unexpected exceptions return the standard error shape with `internal_server_error`.
- [x] Public error responses do not expose validation details, stack traces, provider raw errors, database raw errors, request headers, request body, or secrets.
- [x] Backend logs include request ID, method, path, status code, and error code for handled errors.
- [x] Validation error logs include validation details for debugging.
- [x] Unexpected exception logs include stack traces.
- [x] Request completion logs include request ID, method, path, status code, and duration.
- [x] Logging uses Python stdlib `logging` with structured `extra` fields.
- [x] No external logging dependency, JSON formatter, metrics backend, or tracing backend is introduced in this issue.
- [x] Successful response bodies for existing endpoints remain unchanged.
- [x] Web dashboard client changes are out of scope.
- [x] Tests cover app exception mapping, HTTP exception mapping, validation error mapping, unexpected exception mapping, request ID generation, request ID propagation, response headers, and logging behavior.

## Blocked by

- .scratch/first-slice/issues/10-move-geeknews-fetch-failures-into-service-and-global-handlers.md

## Comments

- 2026-05-09: Implemented request ID middleware, standardized API error envelope, HTTP/validation/unexpected exception handlers, and structured stdlib logging fields.
