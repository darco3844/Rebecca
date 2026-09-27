from datetime import datetime

from src.rebecca.memory import Memory
from src.rebecca.brain import Brain
from src.rebecca.cognitive import CognitiveEngine


class Rebecca:
    def __init__(self):
        self.name = "Rebecca"
        self.version = "0.3.0"

        self.memory = Memory()
        self.brain = Brain()

        self.cognitive = CognitiveEngine(
            self.memory,
            self.brain,
        )

    def greet(self):
        hour = datetime.now().hour

        if hour < 12:
            greeting = "Buenos días"
        elif hour < 19:
            greeting = "Buenas tardes"
        else:
            greeting = "Buenas noches"

        return f"{greeting}, Emi. Soy {self.name}. Mi núcleo está funcionando."

    def remember(self, content):
        self.memory.remember(
            content,
            memory_type="user_requested",
            importance=10,
        )

        return "Lo recordaré."

    def recall(self, search_text):
        memories = self.memory.search(search_text)

        if not memories:
            return "No encontré ningún recuerdo relacionado."

        response = "Encontré esto:\n"

        for memory in memories:
            memory_id, content, memory_type, importance, created_at = memory
            response += f"[{memory_id}] {content}\n"

        return response

    def ask_brain(self, prompt):
        return self.brain.ask(prompt)

    def run(self):
        print("=" * 50)
        print(f"{self.name} v{self.version}")
        print("=" * 50)
        print(self.greet())
        print("Memoria: ONLINE")
        print("Cerebro: ONLINE")
        print("Cognición: ONLINE")
        print()

        while True:
            try:
                command = input("Emi > ").strip()

                if command.lower() in {"salir", "exit", "quit"}:
                    print("Rebecca: Hasta luego, Emi.")
                    self.memory.close()
                    break

                if command.lower().startswith("recuerda "):
                    content = command[9:].strip()

                    if content:
                        print(f"Rebecca: {self.remember(content)}")
                    else:
                        print("Rebecca: ¿Qué quieres que recuerde?")

                    continue

                if command.lower().startswith("recuerdas "):
                    search_text = command[10:].strip()

                    if search_text:
                        print(f"Rebecca: {self.recall(search_text)}")
                    else:
                        print("Rebecca: ¿Qué quieres que busque en mi memoria?")

                    continue

                if command:
                    response = self.cognitive.respond(command)
                    print(f"Rebecca: {response}")

            except KeyboardInterrupt:
                print("\nRebecca: Cerrando sesión.")
                self.memory.close()
                break


if __name__ == "__main__":
    rebecca = Rebecca()
    rebecca.run()
