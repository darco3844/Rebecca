from src.rebecca.memory import Memory
from src.rebecca.memory_manager import MemoryManager


def test_memory_manager():
    memory = Memory("data/memory/test_memory_manager.db")
    manager = MemoryManager(memory)

    # Crear
    memory_id = manager.remember(
        "Mi color favorito es morado.",
        memory_type="preference",
        importance=8,
    )

    assert memory_id > 0

    # Buscar
    results = manager.search("color favorito")

    assert len(results) > 0
    assert any(
        result[0] == memory_id
        for result in results
    )

    # Leer
    saved_memory = manager.get_memory(memory_id)

    assert saved_memory is not None
    assert saved_memory[1] == "Mi color favorito es morado."

    # Actualizar
    updated = manager.update(
        memory_id,
        content="Mi color favorito es azul.",
    )

    assert updated is True

    updated_memory = manager.get_memory(memory_id)

    assert updated_memory is not None
    assert updated_memory[1] == "Mi color favorito es azul."

    # Olvidar
    manager.forget(memory_id)

    forgotten_memory = manager.get_memory(memory_id)

    assert forgotten_memory is None

    memory.close()


if __name__ == "__main__":
    test_memory_manager()
    print("Test MemoryManager: OK")
