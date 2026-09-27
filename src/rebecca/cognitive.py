class CognitiveEngine:
    def __init__(self, memory, brain):
        self.memory = memory
        self.brain = brain

    def respond(self, user_input):
        memories = self.memory.search(user_input, limit=5)

        context = ""

        if memories:
            context = "\n\nRecuerdos relevantes del usuario:\n"

            for memory in memories:
                memory_id, content, memory_type, importance, created_at = memory

                context += f"- {content}\n"

        prompt = f"""
Eres Rebecca, un asistente personal local.

Tu usuario se llama Emi.

Responde de forma natural, clara y breve.
Habla siempre en español.
No inventes recuerdos.
Si los recuerdos proporcionados no contienen la información necesaria,
di honestamente que no la recuerdas.

{context}

Mensaje de Emi:
{user_input}

Respuesta de Rebecca:
"""

        return self.brain.ask(prompt)
