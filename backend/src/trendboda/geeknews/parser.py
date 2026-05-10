# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false

from collections.abc import Mapping
from datetime import UTC, datetime
from re import search
from urllib.parse import parse_qs, urlparse

import feedparser

from trendboda.geeknews.html_text import html_to_text
from trendboda.geeknews.types import GeekNewsItem


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
        content_text = html_to_text(content_raw_html)
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


def _entry_value(entry: object, key: str) -> object | None:
    if isinstance(entry, Mapping):
        return entry.get(key)
    return None
