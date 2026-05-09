import pytest

from trendboda.geeknews import parse_geeknews_rss


def test_parse_geeknews_rss_normalizes_feed_items() -> None:
    rss = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <item>
          <guid>item-1</guid>
          <title>FastAPI &amp; asyncpg</title>
          <link>https://news.example.com/1</link>
          <pubDate>Sat, 09 May 2026 10:30:00 GMT</pubDate>
        </item>
      </channel>
    </rss>
    """

    items = parse_geeknews_rss(rss)

    assert len(items) == 1
    assert items[0].external_id == "item-1"
    assert items[0].title == "FastAPI & asyncpg"
    assert items[0].source_url == "https://news.example.com/1"
    assert items[0].published_at is not None
    assert items[0].published_at.isoformat() == "2026-05-09T10:30:00+00:00"


def test_parse_geeknews_rss_uses_link_when_guid_missing() -> None:
    rss = """<rss><channel><item><title>Title</title><link>https://news.example.com/a</link></item></channel></rss>"""

    items = parse_geeknews_rss(rss)

    assert items[0].external_id == "https://news.example.com/a"


def test_parse_geeknews_rss_rejects_malformed_xml() -> None:
    with pytest.raises(ValueError, match="malformed GeekNews RSS"):
        parse_geeknews_rss("<rss><channel><item></rss>")
