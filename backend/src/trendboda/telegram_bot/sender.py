import httpx


class TelegramSender:
    def __init__(
        self,
        *,
        token: str,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(
            base_url=f"https://api.telegram.org/bot{token}",
            timeout=30,
        )

    async def send_message(self, *, chat_id: int, text: str) -> None:
        response = await self._client.post("/sendMessage", json={"chat_id": chat_id, "text": text})
        response.raise_for_status()

    async def send_payload(self, payload: dict[str, object]) -> None:
        response = await self._client.post("/sendMessage", json=payload)
        response.raise_for_status()

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()
