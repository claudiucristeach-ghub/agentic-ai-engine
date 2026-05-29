"""Tools for the summarizer agent."""

import re
from html.parser import HTMLParser

import httpx
import structlog

logger = structlog.get_logger(__name__)

_MAX_CHARS = 20_000          # cap fetched text so it doesn't blow the context window
_TIMEOUT = 15.0              # seconds
_USER_AGENT = "Mozilla/5.0 (compatible; AgenticAI-Summarizer/1.0)"


class _TextExtractor(HTMLParser):
    """Collect visible text from HTML, skipping script/style/head noise."""

    # Elements whose *text content* should be dropped. Void elements like <meta>
    # / <link> are NOT listed here: they have no end tag, so counting them would
    # leave the skip depth permanently elevated and swallow the whole page.
    _SKIP = {"script", "style", "noscript", "template", "svg"}

    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip_depth = 0
        self._in_title = False
        self.title: str | None = None

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in self._SKIP:
            self._skip_depth += 1
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = data.strip()
        if not text:
            return
        if self._in_title:
            if not self.title:
                self.title = text
            return
        self._chunks.append(text)

    def get_text(self) -> str:
        return re.sub(r"\n{3,}", "\n\n", "\n".join(self._chunks))


async def fetch_url(url: str) -> dict:
    """Fetch a web page and return its readable text content.

    Use this to retrieve the content of a specific URL the user gives you (or one
    you found via google_search) so you can summarize or reason over the page.

    Args:
        url: The full URL to fetch, including the scheme
            (e.g. "https://example.com/article"). If the scheme is missing,
            "https://" is assumed.

    Returns:
        A dict with keys: 'url' (final URL after redirects), 'status' (HTTP status
        code), 'content_type', 'title' (page title if found), 'text' (extracted
        readable text, truncated if very long), and 'truncated' (bool). On
        failure the dict contains an 'error' key instead.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=_TIMEOUT,
            headers={"User-Agent": _USER_AGENT},
        ) as client:
            resp = await client.get(url)
    except Exception as e:
        logger.warning("fetch_url failed", url=url, error=str(e))
        return {"url": url, "error": f"Could not fetch the page: {e}"}

    content_type = resp.headers.get("content-type", "")
    if "html" in content_type.lower():
        parser = _TextExtractor()
        try:
            parser.feed(resp.text)
        except Exception:  # malformed HTML – fall back to raw text
            pass
        text = parser.get_text() or resp.text
        title = parser.title
    else:
        text = resp.text
        title = None

    truncated = len(text) > _MAX_CHARS
    if truncated:
        text = text[:_MAX_CHARS] + "\n\n[... truncated ...]"

    logger.info("fetch_url ok", url=str(resp.url), status=resp.status_code, chars=len(text))
    return {
        "url": str(resp.url),
        "status": resp.status_code,
        "content_type": content_type,
        "title": title,
        "text": text,
        "truncated": truncated,
    }