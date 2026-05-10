import time
from collections.abc import Mapping
from typing import cast

import httpx

from trendboda.ai.json import json_object, mapping, optional_int, optional_str
from trendboda.ai.types import OPENROUTER_BASE_URL, AIUsageStatus, OpenRouterResult


class OpenRouterGateway:
    def __init__(
        self,
        *,
        api_key: str,
        http_client: httpx.AsyncClient | None = None,
        base_url: str = OPENROUTER_BASE_URL,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(timeout=30.0)

    async def complete(
        self,
        *,
        models: list[str],
        messages: list[dict[str, str]],
    ) -> OpenRouterResult:
        started = time.perf_counter()
        try:
            response = await self._client.post(
                f"{self._base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json={"models": models, "messages": messages},
            )
        except httpx.HTTPError as exc:
            return OpenRouterResult(
                status=AIUsageStatus.FAILURE,
                content=None,
                actual_model=None,
                prompt_tokens=None,
                completion_tokens=None,
                total_tokens=None,
                latency_ms=_latency_ms(started),
                error_message=str(exc),
            )

        payload = json_object(response)
        if response.is_error:
            return OpenRouterResult(
                status=AIUsageStatus.FAILURE,
                content=None,
                actual_model=optional_str(payload.get("model")),
                prompt_tokens=None,
                completion_tokens=None,
                total_tokens=None,
                latency_ms=_latency_ms(started),
                error_message=_error_message(payload, response),
            )

        usage = mapping(payload.get("usage"))
        return OpenRouterResult(
            status=AIUsageStatus.SUCCESS,
            content=_content(payload),
            actual_model=optional_str(payload.get("model")),
            prompt_tokens=optional_int(usage.get("prompt_tokens")),
            completion_tokens=optional_int(usage.get("completion_tokens")),
            total_tokens=optional_int(usage.get("total_tokens")),
            latency_ms=_latency_ms(started),
        )

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()


def _content(payload: Mapping[str, object]) -> str | None:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    choice = cast(list[object], choices)[0]
    if not isinstance(choice, Mapping):
        return None
    message = cast(Mapping[str, object], choice).get("message")
    if not isinstance(message, Mapping):
        return None
    return optional_str(cast(Mapping[str, object], message).get("content"))


def _error_message(payload: Mapping[str, object], response: httpx.Response) -> str:
    error = payload.get("error")
    if isinstance(error, Mapping):
        message = optional_str(cast(Mapping[str, object], error).get("message"))
        if message:
            return message
    return f"OpenRouter returned {response.status_code}"


def _latency_ms(started: float) -> int:
    return int((time.perf_counter() - started) * 1000)
