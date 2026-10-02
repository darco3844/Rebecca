from src.rebecca.memory import Memory
from src.rebecca.memory_manager import MemoryManager


def test_memory_v2():
    memory = Memory("data/memory/test_memory_v2.db")
    manager = MemoryManager(memory)

    # Crear un recuerdo con una clave
    memory_id = manager.remember(
        "El color favorito de Emi es morado.",
        memory_type="preference",
        importance=8,
        memory_key="favorite_color",
    )

    assert memory_id > 0

    # Recuperar por clave
    saved = manager.get_by_key("favorite_color")

    assert saved is not None
    assert saved[0] == memory_id
    assert saved[1] == "El color favorito de Emi es morado."

    # Guardar la misma clave con nueva información
    same_id = manager.remember(
        "El color favorito de Emi es azul.",
        memory_type="preference",
        importance=9,
        memory_key="favorite_color",
    )

    # Debe actualizar el recuerdo existente
    assert same_id == memory_id

    # Comprobar actualización
    updated = manager.get_by_key("favorite_color")

    assert updated is not None
    assert updated[0] == memory_id
    assert updated[1] == "El color favorito de Emi es azul."
    assert updated[3] == 9

    # Debe existir solamente un recuerdo con esa clave
    results = manager.search("color favorito")

    matching = [
        result
        for result in results
        if result[5] == "favorite_color"
    ]

    assert len(matching) == 1

    # Olvidar
    manager.forget(memory_id)

    assert manager.get_by_key("favorite_color") is None

    memory.close()


if __name__ == "__main__":
    test_memory_v2()
    print("Test Memory v2: OK")
