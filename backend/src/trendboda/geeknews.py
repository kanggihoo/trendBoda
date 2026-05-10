# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from html import unescape
from html.parser import HTMLParser
from re import search
from urllib.parse import parse_qs, urlparse

import feedparser
import httpx

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


def parse_geeknews_rss(rss_xml: str) -> list[GeekNewsItem]:
    feed = feedparser.parse(rss_xml)
    if feed.bozo:
        raise ValueError("malformed GeekNews RSS")

    items: list[GeekNewsItem] = []
    for entry in feed.entries:
        source_url = str(entry.get("link", "")).strip()
        external_id = _external_id(entry)
        title = str(entry.get("title", "")).strip()
        content_raw_html = _content_raw_html(entry)
        content_text = _html_to_text(content_raw_html)
        published_at = _published_at(entry)

        if not external_id or not title or not source_url:
            continue

        items.append(
            GeekNewsItem(
                external_id=external_id,
                title=title,
                source_url=source_url,
                content_raw_html=content_raw_html,
                content_text=content_text,
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


def _external_id(entry: object) -> str:
    candidates = (
        str(_entry_value(entry, "id") or "").strip(),
        str(_entry_value(entry, "guid") or "").strip(),
        str(_entry_value(entry, "link") or "").strip(),
    )
    for candidate in candidates:
        external_id = _extract_numeric_id(candidate)
        if external_id:
            return external_id
    return ""


def _extract_numeric_id(value: str) -> str:
    if value.isdigit():
        return value

    parsed = urlparse(value)
    query_id = parse_qs(parsed.query).get("id")
    if query_id:
        candidate = query_id[0].strip()
        if candidate.isdigit():
            return candidate

    match = search(r"\b(\d+)\b", value)
    if match is not None:
        return match.group(1)
    return ""


def _content_raw_html(entry: object) -> str:
    content = _entry_value(entry, "content")
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict):
                value = str(item.get("value", "")).strip()
                if value:
                    return value

    summary_detail = _entry_value(entry, "summary_detail")
    if isinstance(summary_detail, dict):
        value = str(summary_detail.get("value", "")).strip()
        if value:
            return value

    summary = str(_entry_value(entry, "summary") or "").strip()
    if summary:
        return summary

    return ""


class _HtmlTextExtractor(HTMLParser):
    _BLOCK_TAGS = {"p", "div", "section", "article", "header", "footer", "blockquote"}
    _LIST_TAGS = {"ul", "ol"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._parts: list[str] = []
        self._ignore_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self._ignore_depth += 1
            return
        if self._ignore_depth > 0:
            return
        if tag == "br":
            self._parts.append("\n")
        elif tag == "li":
            self._append_line_break()
            self._parts.append("• ")
        elif tag in self._BLOCK_TAGS or tag in self._LIST_TAGS:
            self._append_line_break()

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._ignore_depth > 0:
            self._ignore_depth -= 1
            return
        if self._ignore_depth > 0:
            return
        if tag == "li" or tag in self._BLOCK_TAGS or tag in self._LIST_TAGS:
            self._append_line_break()

    def handle_data(self, data: str) -> None:
        if self._ignore_depth > 0:
            return
        self._parts.append(data)

    def handle_entityref(self, name: str) -> None:
        if self._ignore_depth > 0:
            return
        self._parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self._ignore_depth > 0:
            return
        self._parts.append(f"&#{name};")

    def get_text(self) -> str:
        text = unescape("".join(self._parts))
        lines = [" ".join(line.split()) for line in text.splitlines()]
        cleaned_lines = [line for line in lines if line]
        return "\n".join(cleaned_lines).strip()

    def _append_line_break(self) -> None:
        if not self._parts:
            return
        if self._parts[-1] != "\n":
            self._parts.append("\n")


def _html_to_text(value: str) -> str:
    if not value:
        return ""
    parser = _HtmlTextExtractor()
    parser.feed(value)
    parser.close()
    return parser.get_text()


def _entry_value(entry: object, key: str) -> object | None:
    if isinstance(entry, Mapping):
        return entry.get(key)
    return None
