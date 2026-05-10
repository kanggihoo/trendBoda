import httpx

from trendboda.geeknews.parser import parse_geeknews_rss
from trendboda.geeknews.types import GEEKNEWS_FEED_URL, GeekNewsItem


class GeekNewsProvider:
    def __init__(self, feed_url: str = GEEKNEWS_FEED_URL) -> None:
        self._feed_url = feed_url

    async def fetch_items(self) -> list[GeekNewsItem]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self._feed_url)
            response.raise_for_status()
        return parse_geeknews_rss(response.text)
