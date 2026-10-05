from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from src.rebecca.tools.tool import Tool


class PageTextParser(HTMLParser):
    SKIP_TAGS = {
        "script",
        "style",
        "noscript",
        "svg",
        "canvas",
        "template",
    }

    BLOCK_TAGS = {
        "article",
        "section",
        "main",
        "div",
        "p",
        "br",
        "li",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "tr",
    }

    def __init__(self):
        super().__init__()

        self.parts = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return

        if self.skip_depth > 0:
            return

        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            if self.skip_depth > 0:
                self.skip_depth -= 1

            return

        if self.skip_depth > 0:
            return

        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip_depth > 0:
            return

        text = " ".join(
            data.split()
        )

        if text:
            self.parts.append(text)

    def get_text(self):
        text = " ".join(
            self.parts
        )

        lines = []

        for line in text.splitlines():
            line = " ".join(
                line.split()
            )

            if line:
                lines.append(line)

        return "\n".join(lines)


class WebOpenTool(Tool):
    name = "web_open"

    description = (
        "Abre una página web mediante una URL o un "
        "resultado de búsqueda anterior y extrae "
        "su contenido textual."
    )

    permission = "read"

    def prepare_arguments(
        self,
        user_input,
        file_path_extractor=None,
        previous_result=None,
    ):
        url = self._extract_url(
            user_input
        )

        if url:
            return {
                "url": url
            }

        result_number = (
            self._extract_result_number(
                user_input
            )
        )

        if result_number is not None:
            url = self._get_search_result_url(
                previous_result,
                result_number,
            )

            if url:
                return {
                    "url": url
                }

            return {
                "url": "",
                "error": (
                    f"No existe el resultado "
                    f"{result_number} en la última búsqueda."
                ),
            }

        return {
            "url": "",
            "error": (
                "No pude determinar qué página abrir."
            ),
        }

    def run(
        self,
        url,
        max_characters=2500,
        error=None,
    ):
        if error:
            return {
                "error": error
            }

        url = url.strip()

        if not url:
            return {
                "error": (
                    "No se pudo determinar la URL."
                )
            }

        if not self._is_valid_url(url):
            return {
                "error": (
                    "La URL no es válida. "
                    "Debe comenzar con http:// o https://."
                )
            }

        try:
            html, final_url, content_type = (
                self._download_page(url)
            )

            parser = PageTextParser()

            parser.feed(html)
            parser.close()

            text = parser.get_text()

            if not text:
                return {
                    "error": (
                        "La página no contiene texto "
                        "que pueda extraer."
                    ),
                    "url": final_url,
                }

            truncated = len(text) > max_characters

            if truncated:
                text = text[
                    :max_characters
                ].rstrip()

            return {
                "url": final_url,
                "content_type": content_type,
                "text": text,
                "characters": len(text),
                "truncated": truncated,
            }

        except Exception as error:
            return {
                "error": (
                    f"No pude abrir la página: "
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
                "No pude abrir la página:\n"
                f"{result['error']}"
            )

        url = result.get(
            "url",
            "",
        )

        text = result.get(
            "text",
            "",
        )

        if not text:
            return (
                "La página se abrió, pero "
                "no pude extraer contenido."
            )

        notice = ""

        if result.get("truncated"):
            notice = (
                "\n\n[Contenido recortado por longitud.]"
            )

        return (
            f"Página abierta:\n{url}\n\n"
            f"{text}"
            f"{notice}"
        )

    def _download_page(
        self,
        url,
    ):
        headers = {
            "User-Agent": (
                "Rebecca/0.1 "
                "(personal local assistant; "
                "web retrieval)"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,*/*;q=0.8"
            ),
            "Accept-Language": (
                "es-MX,es;q=0.9,en;q=0.7"
            ),
        }

        request = Request(
            url,
            headers=headers,
            method="GET",
        )

        try:
            with urlopen(
                request,
                timeout=15,
            ) as response:
                final_url = response.geturl()

                content_type = response.headers.get(
                    "Content-Type",
                    "",
                )

                if (
                    "text/html" not in content_type
                    and "application/xhtml+xml"
                    not in content_type
                ):
                    raise ValueError(
                        "La URL no apunta a una página HTML."
                    )

                data = response.read()

                charset = response.headers.get_content_charset()

                if not charset:
                    charset = "utf-8"

                html = data.decode(
                    charset,
                    errors="replace",
                )

                return (
                    html,
                    final_url,
                    content_type,
                )

        except HTTPError as error:
            if error.code != 400:
                raise

            retry_headers = {
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/140.0.0.0 Safari/537.36"
                ),
                "Accept": (
                    "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,image/avif,"
                    "image/webp,*/*;q=0.8"
                ),
                "Accept-Language": (
                    "es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7"
                ),
            }

            retry_request = Request(
                url,
                headers=retry_headers,
                method="GET",
            )

            with urlopen(
                retry_request,
                timeout=15,
            ) as response:
                final_url = response.geturl()

                content_type = response.headers.get(
                    "Content-Type",
                    "",
                )

                if (
                    "text/html" not in content_type
                    and "application/xhtml+xml"
                    not in content_type
                ):
                    raise ValueError(
                        "La URL no apunta a una página HTML."
                    )

                data = response.read()

                charset = response.headers.get_content_charset()

                if not charset:
                    charset = "utf-8"

                html = data.decode(
                    charset,
                    errors="replace",
                )

                return (
                    html,
                    final_url,
                    content_type,
                )

        except URLError:
            raise

    def _extract_url(
        self,
        text,
    ):
        words = text.split()

        for word in words:
            candidate = word.strip(
                " \t\n\r.,;:!?()[]{}<>\"'"
            )

            if self._is_valid_url(
                candidate
            ):
                return candidate

        return ""

    def _extract_result_number(
        self,
        text,
    ):
        normalized = (
            text.lower()
            .strip()
        )

        patterns = (
            r"resultado\s+(\d+)",
            r"resultado\s+n[uú]mero\s+(\d+)",
            r"resultado\s+no\.\s*(\d+)",
            r"resultado\s+#\s*(\d+)",
        )

        import re

        for pattern in patterns:
            match = re.search(
                pattern,
                normalized,
            )

            if match:
                return int(
                    match.group(1)
                )

        return None

    def _get_search_result_url(
        self,
        previous_result,
        result_number,
    ):
        if not isinstance(
            previous_result,
            dict,
        ):
            return ""

        if previous_result.get(
            "tool_name"
        ) != "web_search":
            return ""

        result = previous_result.get(
            "result"
        )

        if not isinstance(
            result,
            dict,
        ):
            return ""

        results = result.get(
            "results",
            [],
        )

        index = result_number - 1

        if index < 0 or index >= len(results):
            return ""

        item = results[index]

        if not isinstance(
            item,
            dict,
        ):
            return ""

        return item.get(
            "url",
            "",
        ).strip()

    def _is_valid_url(
        self,
        url,
    ):
        try:
            parsed = urlparse(
                url
            )

            return (
                parsed.scheme in (
                    "http",
                    "https",
                )
                and bool(
                    parsed.netloc
                )
            )

        except ValueError:
            return False

