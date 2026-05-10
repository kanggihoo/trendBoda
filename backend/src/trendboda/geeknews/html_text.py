from html import unescape
from html.parser import HTMLParser


class HtmlTextExtractor(HTMLParser):
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


def html_to_text(value: str) -> str:
    if not value:
        return ""
    parser = HtmlTextExtractor()
    parser.feed(value)
    parser.close()
    return parser.get_text()
