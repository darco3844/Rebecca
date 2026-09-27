from src.rebecca.memory import Memory


memory = Memory("data/memory/test.db")

print("Guardando recuerdo...")

memory.remember(
    "Mi proyecto de asistente de IA se llama Rebecca.",
    memory_type="project",
    importance=10
)

print("Recuerdo guardado.")

print("\nBuscando recuerdo...")

results = memory.search("Rebecca")

for result in results:
    print(result)

memory.close()
