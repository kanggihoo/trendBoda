from dataclasses import dataclass
from datetime import datetime

GEEKNEWS_SOURCE_NAME = "geeknews"
GEEKNEWS_FEED_URL = "https://feeds.feedburner.com/geeknews-feed"


@dataclass(frozen=True)
class GeekNewsItem:
    external_id: str
    title: str
    source_url: str
    content_raw_html: str
    content_text: str
    published_at: datetime | None


@dataclass(frozen=True)
class StoredGeekNewsItem:
    id: int
    fetch_run_id: int | None
    external_id: str
    title: str
    source_url: str
    content_text: str
    published_at: datetime | None
    fetched_at: datetime
