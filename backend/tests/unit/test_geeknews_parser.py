import pytest
from trendboda.geeknews import parse_geeknews_rss

# 테스트용 Atom XML 샘플들
SAMPLE_ATOM_1 = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title><![CDATA[ LLM은 위임할 때 문서를 훼손한다 ]]></title>
    <link rel="alternate" type="text/html" href="https://news.hada.io/topic?id=29351"/>
    <id>https://news.hada.io/topic?id=29351</id>
    <published>2026-05-10T12:33:26+09:00</published>
    <content type="html"><![CDATA[ <ul><li>벤치마크 내용...</li></ul> ]]></content>
  </entry>
</feed>"""

SAMPLE_ATOM_2 = """<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>이름에 대한 오해들</title>
    <link href="https://news.hada.io/topic?id=29350"/>
    <id>29350</id>
    <published>2026-05-10T11:59:58+09:00</published>
    <summary>사람의 이름은 하나가 아니다.</summary>
  </entry>
</feed>"""

SAMPLE_ATOM_3 = """<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>29352</id>
    <title>AI Native 팀의 변화</title>
    <link href="https://news.hada.io/topic?id=29352"/>
    <content type="html" xml:lang="ko">
      <![CDATA[ <ul> <li>소프트웨어 개발이 <strong>결정론적 시스템에서 확률적 시스템으로</strong> 조용히 전환되고 있으며...</li> </ul> ]]>
    </content>
  </entry>
</feed>"""

@pytest.mark.parametrize("xml_input, expected_id, expected_title, expected_text", [
    (SAMPLE_ATOM_1, "29351", "LLM은 위임할 때 문서를 훼손한다", "벤치마크 내용..."),
    (SAMPLE_ATOM_2, "29350", "이름에 대한 오해들", "사람의 이름은 하나가 아니다."),
    (SAMPLE_ATOM_3, "29352", "AI Native 팀의 변화", "소프트웨어 개발이 결정론적 시스템에서 확률적 시스템으로"),
])
def test_parse_geeknews_rss_variants(xml_input, expected_id, expected_title, expected_text):
    items = parse_geeknews_rss(xml_input)
    
    assert len(items) == 1
    assert items[0].external_id == expected_id
    assert items[0].title == expected_title
    assert expected_text in items[0].content_text

def test_parse_geeknews_rss_preserves_order():
    xml = """<feed xmlns="http://www.w3.org/2005/Atom">
      <entry><id>1</id><title>First</title><link href="h1"/></entry>
      <entry><id>2</id><title>Second</title><link href="h2"/></entry>
    </feed>"""
    items = parse_geeknews_rss(xml)
    assert [i.external_id for i in items] == ["1", "2"]

def test_parse_geeknews_rss_rejects_malformed():
    with pytest.raises(ValueError, match="malformed GeekNews RSS"):
        parse_geeknews_rss("<feed><entry></feed>")
