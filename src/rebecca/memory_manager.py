class MemoryManager:
    def __init__(self, memory):
        self.memory = memory

    def remember(
        self,
        content,
        memory_type="general",
        importance=5,
        memory_key=None,
        memory_level="long_term",
    ):
        return self.memory.remember(
            content,
            memory_type=memory_type,
            importance=importance,
            memory_key=memory_key,
            memory_level=memory_level,
        )

    def search(self, text, limit=10):
        return self.memory.search(
            text,
            limit=limit,
        )

    def recent(self, limit=10):
        return self.memory.recent(
            limit=limit,
        )

    def get_memory(self, memory_id):
        memories = self.memory.recent(limit=100000)

        for memory in memories:
            if memory[0] == memory_id:
                return memory

        return None

    def get_by_key(self, memory_key):
        return self.memory.get_by_key(memory_key)

    def update(
        self,
        memory_id,
        content=None,
        memory_type=None,
        importance=None,
        memory_key=None,
        memory_level=None,
    ):
        return self.memory.update(
            memory_id,
            content=content,
            memory_type=memory_type,
            importance=importance,
            memory_key=memory_key,
            memory_level=memory_level,
        )

    def forget(self, memory_id):
        self.memory.forget(memory_id)

    def count(self):
        memories = self.memory.recent(limit=100000)
        return len(memories)
