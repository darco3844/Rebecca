from datetime import datetime
import re


class WorkingMemory:
    def __init__(self, max_items=10):
        self.max_items = max_items
        self.items = []

    def add(
        self,
        content,
        importance=5,
    ):
        item = {
            "content": content,
            "importance": importance,
            "created_at": datetime.now().isoformat(),
        }

        self.items.append(item)

        self._trim()

    def get_all(self):
        return list(self.items)

    def get_relevant(self, limit=5):
        ordered = sorted(
            self.items,
            key=lambda item: (
                item["importance"],
                item["created_at"],
            ),
            reverse=True,
        )

        return ordered[:limit]

    def search(self, text, limit=5):
        query_words = self._keywords(text)

        if not query_words:
            return self.get_relevant(limit)

        matches = []

        for item in self.items:
            content_words = self._keywords(
                item["content"]
            )

            score = sum(
                1
                for word in query_words
                if word in content_words
            )

            if score > 0:
                matches.append(
                    (
                        score,
                        item,
                    )
                )

        matches.sort(
            key=lambda pair: (
                pair[0],
                pair[1]["importance"],
                pair[1]["created_at"],
            ),
            reverse=True,
        )

        return [
            item
            for _, item in matches[:limit]
        ]

    def remove(self, content):
        self.items = [
            item
            for item in self.items
            if item["content"] != content
        ]

    def clear(self):
        self.items.clear()

    def count(self):
        return len(self.items)

    def _keywords(self, text):
        words = re.findall(
            r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]+",
            text.lower(),
        )

        stopwords = {
            "que",
            "qué",
            "como",
            "cómo",
            "de",
            "del",
            "la",
            "el",
            "los",
            "las",
            "un",
            "una",
            "y",
            "o",
            "a",
            "por",
            "para",
            "con",
            "mi",
            "mis",
            "tu",
            "tus",
            "yo",
            "me",
            "te",
            "es",
            "son",
            "en",
            "recuerdas",
            "recuerdo",
        }

        return {
            word
            for word in words
            if word not in stopwords
            and len(word) > 2
        }

    def _trim(self):
        if len(self.items) <= self.max_items:
            return

        self.items = sorted(
            self.items,
            key=lambda item: (
                item["importance"],
                item["created_at"],
            ),
            reverse=True,
        )[:self.max_items]
