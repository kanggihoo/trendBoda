# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false

from dataclasses import dataclass
from datetime import UTC, datetime

import feedparser
import httpx

GEEKNEWS_SOURCE_NAME = "geeknews"
GEEKNEWS_FEED_URL = "https://feeds.feedburner.com/geeknews-feed"


@dataclass(frozen=True)
class GeekNewsItem:
    external_id: str
    title: str
    source_url: str
    published_at: datetime | None


@dataclass(frozen=True)
class StoredGeekNewsItem:
    id: int
    fetch_run_id: int | None
    external_id: str
    title: str
    source_url: str
    published_at: datetime | None
    fetched_at: datetime


def parse_geeknews_rss(rss_xml: str) -> list[GeekNewsItem]:
    feed = feedparser.parse(rss_xml)
    if feed.bozo:
        raise ValueError("malformed GeekNews RSS")

    items: list[GeekNewsItem] = []
    for entry in feed.entries:
        source_url = str(entry.get("link", "")).strip()
        external_id = str(entry.get("id") or entry.get("guid") or source_url).strip()
        title = str(entry.get("title", "")).strip()
        published_at = _published_at(entry)

        if not external_id or not title or not source_url:
            continue

        items.append(
            GeekNewsItem(
                external_id=external_id,
                title=title,
                source_url=source_url,
                published_at=published_at,
            )
        )

    return items


class GeekNewsProvider:
    def __init__(self, feed_url: str = GEEKNEWS_FEED_URL) -> None:
        self._feed_url = feed_url

    async def fetch_items(self) -> list[GeekNewsItem]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self._feed_url)
            response.raise_for_status()
        return parse_geeknews_rss(response.text)


def _published_at(entry: object) -> datetime | None:
    published = getattr(entry, "published_parsed", None)
    if published is None:
        return None
    return datetime(*published[:6], tzinfo=UTC)
