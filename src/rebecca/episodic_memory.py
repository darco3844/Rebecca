from datetime import datetime


class EpisodicMemory:
    def __init__(self, memory):
        self.memory = memory

    def record(
        self,
        event,
        importance=5,
    ):
        event = event.strip()

        if not event:
            return None

        existing = self._find_duplicate(
            event
        )

        if existing:
            return existing[0]

        timestamp = datetime.now().isoformat()

        content = (
            f"Evento: {event} "
            f"[fecha: {timestamp}]"
        )

        return self.memory.remember(
            content,
            memory_type="episode",
            importance=importance,
            memory_level="long_term",
        )

    def search(
        self,
        text,
        limit=10,
    ):
        memories = self.memory.search(
            text,
            limit=limit,
        )

        return [
            memory
            for memory in memories
            if memory[2] == "episode"
        ]

    def recent(self, limit=10):
        memories = self.memory.recent(
            limit=limit
        )

        return [
            memory
            for memory in memories
            if memory[2] == "episode"
        ]

    def get(self, memory_id):
        memories = self.memory.recent(
            limit=100000
        )

        for memory in memories:
            if (
                memory[0] == memory_id
                and memory[2] == "episode"
            ):
                return memory

        return None

    def forget(self, memory_id):
        episode = self.get(memory_id)

        if episode is None:
            return False

        self.memory.forget(
            memory_id
        )

        return True

    def _find_duplicate(self, event):
        memories = self.memory.search(
            event,
            limit=20,
        )

        marker = f"Evento: {event}"

        for memory in memories:
            if (
                memory[2] == "episode"
                and memory[1].startswith(marker)
            ):
                return memory

        return None
