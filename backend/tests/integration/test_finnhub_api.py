from typing import Any

import httpx
import pytest

from trendboda.config import get_settings

FINNHUB_BASE_URL = "https://finnhub.io/api/v1"


@pytest.mark.integration
@pytest.mark.parametrize("symbol", ["AAPL", "NVDA", "SPY", "QQQ"])
async def test_finnhub_quote_returns_price_snapshot_fields(symbol: str) -> None:
    token = get_settings().finnhub_api_key
    if not token:
        pytest.skip("FINNHUB_API_KEY is not configured")

    async with httpx.AsyncClient(base_url=FINNHUB_BASE_URL, timeout=10.0) as client:
        response = await client.get("/quote", params={"symbol": symbol, "token": token})

    assert response.status_code == 200
    payload: dict[str, Any] = response.json()

    assert set(payload) >= {"c", "d", "dp", "h", "l", "o", "pc", "t"}
    assert payload["c"] > 0
    assert payload["pc"] > 0
    assert payload["t"] > 0


@pytest.mark.integration
async def test_finnhub_quote_invalid_symbol_shape() -> None:
    token = get_settings().finnhub_api_key
    if not token:
        pytest.skip("FINNHUB_API_KEY is not configured")

    async with httpx.AsyncClient(base_url=FINNHUB_BASE_URL, timeout=10.0) as client:
        response = await client.get(
            "/quote",
            params={"symbol": "BADSYMBOL_DO_NOT_USE", "token": token},
        )

    assert response.status_code == 200
    payload: dict[str, Any] = response.json()

    assert set(payload) >= {"c", "d", "dp", "h", "l", "o", "pc", "t"}
    assert payload["c"] == 0
    assert payload["pc"] == 0
    assert payload["t"] == 0
