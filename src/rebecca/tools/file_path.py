import re


class FilePathExtractor:
    def extract(self, text):
        text = text.strip()

        match = re.search(
            r"(~\/[^\s?]+|\/[^\s?]+)",
            text,
        )

        if match:
            return match.group(1).rstrip(".,;:")

        match = re.search(
            r"\b([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+)\b",
            text,
        )

        if match:
            return match.group(1).rstrip(".,;:")

        match = re.search(
            r"(?:archivo|carpeta|directorio)\s+([A-Za-z0-9_.~-]+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1).rstrip(".,;:")

        return "."
