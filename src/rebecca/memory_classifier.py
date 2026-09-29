class MemoryClassifier:
    def classify(self, content):
        text = content.lower()

        # Preferencias
        if any(
            phrase in text
            for phrase in [
                "me gusta",
                "me encanta",
                "prefiero",
                "mi favorito",
                "mi favorita",
                "mi color favorito",
                "mi música favorita",
                "mi musica favorita",
                "mi comida favorita",
                "no me gusta",
            ]
        ):
            return "preference"

        # Proyecto Rebecca
        if any(
            phrase in text
            for phrase in [
                "mi proyecto",
                "proyecto rebecca",
                "rebecca",
                "estamos construyendo",
                "cachyos",
                "qwen",
                "qwen3",
                "llama-server",
                "llama server",
            ]
        ):
            return "project"

        # Objetivos
        if any(
            phrase in text
            for phrase in [
                "mi objetivo",
                "quiero lograr",
                "quiero conseguir",
                "mi meta",
                "quiero construir",
                "quiero crear",
            ]
        ):
            return "goal"

        # Relaciones
        if any(
            phrase in text
            for phrase in [
                "mi esposa",
                "mi amigo",
                "mi amiga",
                "mi familia",
            ]
        ):
            return "relationship"

        # Configuración
        if any(
            phrase in text
            for phrase in [
                "uso",
                "tengo instalado",
                "está instalado",
                "esta instalado",
                "configuración",
                "configuracion",
                "configurado",
            ]
        ):
            return "configuration"

        return "general"

    def generate_key(self, content, memory_type):
        text = content.lower()

        if memory_type == "preference":
            if "color" in text:
                return "favorite_color"

            if "música" in text or "musica" in text:
                return "music_preference"

            if "comida" in text:
                return "food_preference"

            return "general_preference"

        if memory_type == "project":
            if "nombre" in text and "proyecto" in text:
                return "project_name"

            if "cachyos" in text:
                return "project_os"

            if "qwen" in text:
                return "project_model"

            if "llama" in text:
                return "project_inference"

            return "project_fact"

        if memory_type == "goal":
            return "goal"

        if memory_type == "relationship":
            return "relationship"

        if memory_type == "configuration":
            return "configuration"

        return None
