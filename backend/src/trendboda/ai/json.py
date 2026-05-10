from collections.abc import Mapping
from decimal import Decimal
from typing import cast

import httpx


def json_object(response: httpx.Response) -> dict[str, object]:
    try:
        payload: object = response.json()
    except ValueError:
        return {}
    if isinstance(payload, dict):
        return cast(dict[str, object], payload)
    return {}


def mapping(value: object) -> Mapping[str, object]:
    if isinstance(value, Mapping):
        return cast(Mapping[str, object], value)
    return {}


def optional_str(value: object) -> str | None:
    if isinstance(value, str):
        return value
    return None


def optional_int(value: object) -> int | None:
    if isinstance(value, int):
        return value
    return None


def decimal_or_none(value: object) -> Decimal | None:
    if isinstance(value, str | int | float):
        return Decimal(str(value))
    return None
