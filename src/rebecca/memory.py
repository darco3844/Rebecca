import re
import sqlite3
from pathlib import Path
from datetime import datetime


class Memory:
    def __init__(self, database_path="data/memory/rebecca.db"):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.database_path)

        self._create_tables()

    def _create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                importance INTEGER DEFAULT 5,
                created_at TEXT NOT NULL
            )
        """)

        self.connection.commit()

    def remember(self, content, memory_type="general", importance=5):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM memories
            WHERE content = ?
            LIMIT 1
            """,
            (content,),
        )

        existing = cursor.fetchone()

        if existing:
            return existing[0]

        cursor.execute(
            """
            INSERT INTO memories
            (content, memory_type, importance, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                content,
                memory_type,
                importance,
                datetime.now().isoformat(),
            ),
        )

        self.connection.commit()

        return cursor.lastrowid

    def search(self, text, limit=10):
        words = re.findall(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]+", text.lower())

        stopwords = {
            "que",
            "qué",
            "como",
            "cómo",
            "cual",
            "cuál",
            "cuales",
            "cuáles",
            "de",
            "del",
            "la",
            "el",
            "los",
            "las",
            "un",
            "una",
            "unos",
            "unas",
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
            "y",
            "o",
            "a",
            "por",
            "para",
            "con",
            "sobre",
            "recuerdas",
            "recuerdo",
        }

        keywords = [
            word
            for word in words
            if word not in stopwords and len(word) > 2
        ]

        if not keywords:
            return self.recent(limit)

        conditions = " OR ".join(
            ["LOWER(content) LIKE ?" for _ in keywords]
        )

        parameters = [f"%{keyword}%" for keyword in keywords]
        parameters.append(limit)

        cursor = self.connection.cursor()

        cursor.execute(
            f"""
            SELECT id, content, memory_type, importance, created_at
            FROM memories
            WHERE {conditions}
            ORDER BY importance DESC, created_at DESC
            LIMIT ?
            """,
            parameters,
        )

        return cursor.fetchall()

    def recent(self, limit=10):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT id, content, memory_type, importance, created_at
            FROM memories
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()

    def forget(self, memory_id):
        cursor = self.connection.cursor()

        cursor.execute(
            "DELETE FROM memories WHERE id = ?",
            (memory_id,),
        )

        self.connection.commit()

    def close(self):
        self.connection.close()
