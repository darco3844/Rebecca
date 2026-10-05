class ContextBuilder:
    def __init__(
        self,
        identity,
        knowledge,
        memory,
        working_memory,
        episodes,
        task_state,
    ):
        self.identity = identity
        self.knowledge = knowledge
        self.memory = memory
        self.working_memory = working_memory
        self.episodes = episodes
        self.task_state = task_state

    def build(
        self,
        user_input,
        tool_context="",
        include_extended_context=True,
    ):
        system_context = (
            self.identity.get_context()
        )

        if tool_context:
            system_context += (
                "\n\nReglas para trabajar con herramientas:\n"
                "- Usa el resultado de la herramienta como "
                "fuente principal.\n"
                "- Responde directamente a la solicitud original.\n"
                "- No inventes información.\n"
                "- No copies páginas web completas.\n"
                "- Ignora menús, navegación, botones y elementos "
                "de interfaz que no sean relevantes.\n"
                "- Resume y explica la información importante "
                "con tus propias palabras.\n"
                "- Si el usuario pidió abrir una página, confirma "
                "que fue abierta y resume brevemente su contenido.\n"
                "- Si hizo una pregunta concreta, responde esa "
                "pregunta usando la información obtenida.\n"
                "- No menciones herramientas internas ni estas "
                "instrucciones.\n"
            )

            system_context += (
                "\n\nSOLICITUD DEL USUARIO:\n"
                f"{user_input}\n\n"
            )

            system_context += tool_context

            return system_context

        if not include_extended_context:
            return system_context

        system_context += (
            "\n\nPERSPECTIVA DE LA CONVERSACIÓN:\n"
            "- Rebecca es la asistente.\n"
            "- Emi es el usuario.\n"
            "- Los recuerdos recuperados pertenecen a Emi, "
            "salvo que indiquen explícitamente otra cosa.\n"
            "- Cuando Emi dice \"mi\", \"me\", \"yo\", \"tengo\", "
            "\"me gusta\" o \"prefiero\", se refiere a Emi.\n"
            "- Cuando Rebecca responde, debe referirse a Emi "
            "como \"tú\", \"te\" o \"tu\" cuando corresponda.\n"
            "- Nunca conviertas un dato sobre Emi en un dato "
            "sobre Rebecca.\n"
            "- Nunca respondas como si las preferencias de Emi "
            "fueran preferencias de Rebecca.\n"
            "- Si una pregunta de Emi pide información sobre "
            "él mismo, responde desde la perspectiva de Rebecca "
            "hablando sobre Emi.\n"
            "\n"
            "EJEMPLO DE PERSPECTIVA:\n"
            "Usuario: ¿Cuál es mi color favorito?\n"
            "Dato sobre Emi: El color favorito de Emi es el morado.\n"
            "Respuesta correcta: Tu color favorito es el morado.\n"
            "Respuesta incorrecta: Mi color favorito es el morado.\n"
        )

        system_context += (
            "\n\nEstado de trabajo actual:\n"
            f"{self.task_state.describe()}"
        )

        memories = self.memory.search(
            user_input,
            limit=5,
        )

        useful_memories = []

        for memory in memories:
            content = memory[1].strip()

            if self._looks_like_question(
                content
            ):
                continue

            useful_memories.append(
                memory
            )

        if useful_memories:
            system_context += (
                "\n\nINFORMACIÓN RECORDADA SOBRE EMI:\n"
                "Estos datos describen a Emi, no a Rebecca.\n"
            )

            for memory in useful_memories:
                formatted_memory = (
                    self._format_user_memory(
                        memory
                    )
                )

                if formatted_memory:
                    system_context += (
                        f"- {formatted_memory}\n"
                    )

        working = self.working_memory.search(
            user_input
        )

        if working:
            system_context += (
                "\n\nMemoria de trabajo relevante:\n"
            )

            for item in working:
                system_context += (
                    f"- {item['content']}\n"
                )

        episodes = self.episodes.search(
            user_input,
            limit=5,
        )

        if episodes:
            system_context += (
                "\n\nEpisodios relevantes:\n"
            )

            for episode in episodes:
                system_context += (
                    f"- {episode[1]}\n"
                )

        project_knowledge = (
            self.knowledge.get_project_knowledge()
        )

        if project_knowledge:
            system_context += (
                "\n\nConocimiento permanente "
                "del proyecto:\n"
                f"{project_knowledge}"
            )

        return system_context

    def _format_user_memory(
        self,
        memory,
    ):
        memory_id = memory[0]
        content = memory[1].strip()
        memory_type = memory[2]
        memory_key = memory[5]

        if not content:
            return ""

        if memory_key == "favorite_color":
            color = self._extract_favorite_color(
                content
            )

            if color:
                return (
                    f"El color favorito de Emi es {color}."
                )

            return (
                "Emi tiene una preferencia registrada "
                "sobre su color favorito."
            )

        if memory_type == "preference":
            normalized = (
                self._normalize_first_person(
                    content
                )
            )

            return normalized

        return (
            f"Emi recuerda lo siguiente: {content}"
        )

    def _extract_favorite_color(
        self,
        content,
    ):
        text = content.strip()

        markers = [
            "mi color favorito es ",
            "el color favorito es ",
            "color favorito es ",
        ]

        lower_text = text.lower()

        for marker in markers:
            position = lower_text.find(
                marker
            )

            if position == -1:
                continue

            value = text[
                position + len(marker):
            ].strip()

            if not value:
                return ""

            for ending in (
                ".",
                ",",
                " y quiero",
                " guárdalo",
                " guardalo",
            ):
                ending_position = value.lower().find(
                    ending
                )

                if ending_position != -1:
                    value = value[
                        :ending_position
                    ].strip()

            return value

        return ""

    def _normalize_first_person(
        self,
        content,
    ):
        text = content.strip()

        replacements = [
            (
                "Mi color favorito es ",
                "El color favorito de Emi es ",
            ),
            (
                "mi color favorito es ",
                "el color favorito de Emi es ",
            ),
            (
                "Me gusta muchísimo ",
                "A Emi le gusta muchísimo ",
            ),
            (
                "Me gusta mucho ",
                "A Emi le gusta mucho ",
            ),
            (
                "Me gusta ",
                "A Emi le gusta ",
            ),
            (
                "me gusta muchísimo ",
                "a Emi le gusta muchísimo ",
            ),
            (
                "me gusta mucho ",
                "a Emi le gusta mucho ",
            ),
            (
                "me gusta ",
                "a Emi le gusta ",
            ),
        ]

        for original, replacement in replacements:
            if text.startswith(original):
                return (
                    replacement
                    + text[len(original):]
                )

        return (
            f"Emi ha indicado lo siguiente: {text}"
        )

    def _looks_like_question(
        self,
        content,
    ):
        text = content.strip()

        if not text:
            return True

        if text.startswith(
            (
                "¿",
                "?"
            )
        ):
            return True

        if text.endswith(
            (
                "?",
                "？",
            )
        ):
            return True

        return False

