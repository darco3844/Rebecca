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
            system_context += tool_context

        if not include_extended_context:
            return system_context

        system_context += (
            "\n\nEstado de trabajo actual:\n"
            f"{self.task_state.describe()}"
        )

        memories = self.memory.search(
            user_input,
            limit=5,
        )

        if memories:
            system_context += (
                "\n\nRecuerdos relevantes:\n"
            )

            for memory in memories:
                system_context += (
                    f"- {memory[1]}\n"
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
