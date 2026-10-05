from html.parser import HTMLParser
from urllib.parse import (
    parse_qs,
    quote,
    unquote,
    urlparse,
)
from urllib.request import Request, urlopen

from src.rebecca.tools.tool import Tool


class SearchResultParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self.results = []
        self.current_result = None
        self.mode = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)

        classes = set(
            attributes.get(
                "class",
                "",
            ).split()
        )

        if tag == "a" and "result__a" in classes:
            self._start_result(
                attributes.get(
                    "href",
                    "",
                )
            )

            self.mode = "title"
            return

        if (
            self.current_result is not None
            and "result__snippet" in classes
        ):
            self.mode = "snippet"

    def handle_endtag(self, tag):
        if self.mode == "title" and tag == "a":
            self.mode = None

        elif self.mode == "snippet":
            self.mode = None

    def handle_data(self, data):
        if self.current_result is None:
            return

        if self.mode == "title":
            self.current_result["title"] += data

        elif self.mode == "snippet":
            self.current_result["snippet"] += data

    def close(self):
        super().close()

        self._finish_result()

    def _start_result(self, url):
        self._finish_result()

        self.current_result = {
            "title": "",
            "url": url,
            "snippet": "",
        }

    def _finish_result(self):
        if self.current_result is None:
            return

        title = " ".join(
            self.current_result.get(
                "title",
                "",
            ).split()
        )

        snippet = " ".join(
            self.current_result.get(
                "snippet",
                "",
            ).split()
        )

        url = self.current_result.get(
            "url",
            "",
        ).strip()

        if title and url:
            self.results.append(
                {
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                }
            )

        self.current_result = None
        self.mode = None


class WebSearchTool(Tool):
    name = "web_search"

    description = (
        "Busca información actual en Internet y devuelve "
        "resultados con título, URL y fragmento."
    )

    permission = "read"

    def prepare_arguments(
        self,
        user_input,
        file_path_extractor=None,
    ):
        return {
            "query": self._extract_query(
                user_input
            )
        }

    def run(
        self,
        query,
        max_results=5,
    ):
        query = query.strip()

        if not query:
            return {
                "error": (
                    "No se pudo determinar qué buscar."
                )
            }

        try:
            return self._search_duckduckgo(
                query,
                max_results=max_results,
            )

        except Exception as error:
            return {
                "error": (
                    f"No pude realizar la búsqueda: "
                    f"{error}"
                )
            }

    def format_result(
        self,
        result,
        user_input="",
    ):
        if not isinstance(result, dict):
            return None

        if result.get("error"):
            return (
                "No pude realizar la búsqueda:\n"
                f"{result['error']}"
            )

        results = result.get(
            "results",
            [],
        )

        if not results:
            return (
                "No encontré resultados para esa búsqueda."
            )

        lines = [
            (
                "Resultados para: "
                f"{result.get('query', 'la búsqueda')}"
            ),
            "",
        ]

        for index, item in enumerate(
            results,
            start=1,
        ):
            title = item.get(
                "title",
                "Sin título",
            )

            url = item.get(
                "url",
                "",
            )

            snippet = item.get(
                "snippet",
                "",
            )

            lines.append(
                f"{index}. {title}"
            )

            if snippet:
                lines.append(
                    f"   {snippet}"
                )

            if url:
                lines.append(
                    f"   {url}"
                )

            lines.append("")

        return "\n".join(
            lines
        ).strip()

    def _search_duckduckgo(
        self,
        query,
        max_results=5,
    ):
        encoded_query = quote(
            query
        )

        url = (
            "https://html.duckduckgo.com/"
            f"html/?q={encoded_query}"
        )

        request = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/140 Safari/537.36"
                )
            },
        )

        with urlopen(
            request,
            timeout=10,
        ) as response:
            html = response.read().decode(
                "utf-8",
                errors="replace",
            )

        parser = SearchResultParser()

        parser.feed(html)
        parser.close()

        results = []

        for item in parser.results:
            title = item.get(
                "title",
                "",
            ).strip()

            url = self._clean_url(
                item.get(
                    "url",
                    "",
                )
            )

            snippet = item.get(
                "snippet",
                "",
            ).strip()

            if not title or not url:
                continue

            results.append(
                {
                    "title": title,
                    "url": url,
                    "snippet": snippet,
                }
            )

            if len(results) >= max_results:
                break

        return {
            "query": query,
            "provider": "duckduckgo",
            "results": results,
            "count": len(results),
        }

    def _clean_url(self, url):
        url = url.strip()

        if not url:
            return ""

        if url.startswith("//"):
            url = "https:" + url

        parsed = urlparse(
            url
        )

        query = parse_qs(
            parsed.query
        )

        redirected_url = query.get(
            "uddg"
        )

        if redirected_url:
            return unquote(
                redirected_url[0]
            )

        return url

    def _extract_query(
        self,
        text,
    ):
        text = text.strip()

        prefixes = [
            "busca en internet ",
            "buscar en internet ",
            "busca en la web ",
            "buscar en la web ",
            "busca en google ",
            "buscar en google ",
            "buscame en internet ",
            "búscame en internet ",
            "buscame en la web ",
            "búscame en la web ",
            "buscame en google ",
            "búscame en google ",
            "busca ",
            "buscar ",
            "búscame ",
            "buscame ",
            "investiga ",
            "investigar ",
        ]

        lower_text = text.lower()

        for prefix in prefixes:
            if lower_text.startswith(prefix):
                return text[
                    len(prefix):
                ].strip()

        return text

