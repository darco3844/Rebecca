import re
import sqlite3
from pathlib import Path
from datetime import datetime


class Memory:
    def __init__(self, database_path="data/memory/rebecca.db"):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.database_path, check_same_thread=False)

        self._create_tables()
        self._migrate_tables()

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

    def _migrate_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("PRAGMA table_info(memories)")
        columns = [column[1] for column in cursor.fetchall()]

        if "memory_key" not in columns:
            cursor.execute("""
                ALTER TABLE memories
                ADD COLUMN memory_key TEXT
            """)

        if "memory_level" not in columns:
            cursor.execute("""
                ALTER TABLE memories
                ADD COLUMN memory_level TEXT DEFAULT 'long_term'
            """)

        self.connection.commit()

    def remember(
        self,
        content,
        memory_type="general",
        importance=5,
        memory_key=None,
        memory_level="long_term",
    ):
        cursor = self.connection.cursor()

        if memory_key:
            cursor.execute(
                """
                SELECT id
                FROM memories
                WHERE memory_key = ?
                LIMIT 1
                """,
                (memory_key,),
            )

            existing = cursor.fetchone()

            if existing:
                self.update(
                    existing[0],
                    content=content,
                    memory_type=memory_type,
                    importance=importance,
                    memory_key=memory_key,
                    memory_level=memory_level,
                )

                return existing[0]

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
            (
                content,
                memory_type,
                importance,
                created_at,
                memory_key,
                memory_level
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                content,
                memory_type,
                importance,
                datetime.now().isoformat(),
                memory_key,
                memory_level,
            ),
        )

        self.connection.commit()

        return cursor.lastrowid

    def search(self, text, limit=10):
        words = re.findall(
            r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9]+",
            text.lower(),
        )

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

        parameters = [
            f"%{keyword}%"
            for keyword in keywords
        ]

        parameters.append(limit)

        cursor = self.connection.cursor()

        cursor.execute(
            f"""
            SELECT
                id,
                content,
                memory_type,
                importance,
                created_at,
                memory_key,
                memory_level
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
            SELECT
                id,
                content,
                memory_type,
                importance,
                created_at,
                memory_key,
                memory_level
            FROM memories
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )

        return cursor.fetchall()

    def get_by_key(self, memory_key):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                content,
                memory_type,
                importance,
                created_at,
                memory_key,
                memory_level
            FROM memories
            WHERE memory_key = ?
            LIMIT 1
            """,
            (memory_key,),
        )

        return cursor.fetchone()

    def update(
        self,
        memory_id,
        content=None,
        memory_type=None,
        importance=None,
        memory_key=None,
        memory_level=None,
    ):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT
                content,
                memory_type,
                importance,
                memory_key,
                memory_level
            FROM memories
            WHERE id = ?
            """,
            (memory_id,),
        )

        existing = cursor.fetchone()

        if not existing:
            return False

        (
            old_content,
            old_type,
            old_importance,
            old_key,
            old_level,
        ) = existing

        new_content = (
            content
            if content is not None
            else old_content
        )

        new_type = (
            memory_type
            if memory_type is not None
            else old_type
        )

        new_importance = (
            importance
            if importance is not None
            else old_importance
        )

        new_key = (
            memory_key
            if memory_key is not None
            else old_key
        )

        new_level = (
            memory_level
            if memory_level is not None
            else old_level
        )

        cursor.execute(
            """
            UPDATE memories
            SET content = ?,
                memory_type = ?,
                importance = ?,
                memory_key = ?,
                memory_level = ?
            WHERE id = ?
            """,
            (
                new_content,
                new_type,
                new_importance,
                new_key,
                new_level,
                memory_id,
            ),
        )

        self.connection.commit()

        return True

    def forget(self, memory_id):
        cursor = self.connection.cursor()

        cursor.execute(
            "DELETE FROM memories WHERE id = ?",
            (memory_id,),
        )

        self.connection.commit()

    def close(self):
        self.connection.close()
