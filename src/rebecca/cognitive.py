from src.rebecca.conversation import Conversation
from src.rebecca.knowledge import Knowledge
from src.rebecca.identity import Identity
from src.rebecca.memory_manager import MemoryManager
from src.rebecca.intent import IntentDetector
from src.rebecca.memory_classifier import MemoryClassifier


class CognitiveEngine:
    def __init__(self, memory, brain):
        self.memory = MemoryManager(memory)
        self.brain = brain

        self.conversation = Conversation(max_messages=10)
        self.knowledge = Knowledge()
        self.identity = Identity()
        self.intent = IntentDetector()
        self.classifier = MemoryClassifier()

    def respond(self, user_input):
        intent = self.intent.detect(user_input)

        # RECORDAR
        if intent == "remember":
            content = self._extract_memory_content(user_input)

            if not content:
                return "¿Qué quieres que recuerde?"

            memory_type = self.classifier.classify(content)
            memory_key = self.classifier.generate_key(
                content,
                memory_type,
            )

            memory_id = self.memory.remember(
                content,
                memory_type=memory_type,
                importance=10,
                memory_key=memory_key,
            )

            if memory_key:
                return (
                    f"Lo recordaré. Memoria #{memory_id}. "
                    f"Tipo: {memory_type}. "
                    f"Clave: {memory_key}."
                )

            return (
                f"Lo recordaré. Memoria #{memory_id}. "
                f"Tipo: {memory_type}."
            )

        # CONSULTAR MEMORIA
        if intent == "recall_memory":
            memories = self.memory.search(
                user_input,
                limit=10,
            )

            if not memories:
                return "No encontré recuerdos relacionados."

            response = "Esto es lo que recuerdo:\n"

            for memory in memories:
                (
                    memory_id,
                    content,
                    memory_type,
                    importance,
                    created_at,
                    memory_key,
                ) = memory

                response += (
                    f"[{memory_id}] "
                    f"{content} "
                    f"(tipo: {memory_type})\n"
                )

            return response.strip()

        # OLVIDAR
        if intent == "forget_memory":
            words = user_input.split()

            memory_id = None

            for word in words:
                clean_word = word.strip(".,!?¿¡#")

                if clean_word.isdigit():
                    memory_id = int(clean_word)
                    break

            if memory_id is None:
                return (
                    "Necesito el número del recuerdo que quieres olvidar. "
                    "Por ejemplo: 'olvida el recuerdo 12'."
                )

            memory = self.memory.get_memory(memory_id)

            if memory is None:
                return f"No encontré el recuerdo #{memory_id}."

            self.memory.forget(memory_id)

            return (
                f"He olvidado el recuerdo #{memory_id}: "
                f"{memory[1]}"
            )

        # MEMORIA PARA CONVERSACIÓN NORMAL
        memories = self.memory.search(
            user_input,
            limit=5,
        )

        system_context = self.identity.get_context()

        system_context += f"""

Intención detectada:
{intent}

Reglas de respuesta:

Responde directamente al mensaje de Emi.

No repitas la pregunta de Emi antes de responder.

No inventes información.

No inventes recuerdos.

Utiliza los recuerdos proporcionados cuando sean relevantes.

Si la información no está disponible, dilo honestamente.
"""

        if memories:
            system_context += "\nRecuerdos relevantes de Emi:\n"

            for memory in memories:
                (
                    memory_id,
                    content,
                    memory_type,
                    importance,
                    created_at,
                    memory_key,
                ) = memory

                system_context += (
                    f"- {content} "
                    f"(tipo: {memory_type})\n"
                )

        project_knowledge = self.knowledge.get_project_knowledge()

        system_context += "\nConocimiento del proyecto Rebecca:\n"
        system_context += project_knowledge

        messages = [
            {
                "role": "system",
                "content": system_context,
            }
        ]

        self.conversation.add_user_message(user_input)

        for message in self.conversation.get_messages():
            messages.append({
                "role": message["role"],
                "content": message["content"],
            })

        response = self.brain.ask(messages)

        self.conversation.add_assistant_message(response)

        return response

    def _extract_memory_content(self, user_input):
        prefixes = [
            "recuerda ",
            "acuérdate de ",
            "acuerdate de ",
            "guarda ",
        ]

        text = user_input.strip()

        for prefix in prefixes:
            if text.lower().startswith(prefix):
                return text[len(prefix):].strip()

        return text
