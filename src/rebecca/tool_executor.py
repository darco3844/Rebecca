class ToolExecutor:
    def __init__(
        self,
        tool_intent,
        tools,
        file_path_extractor,
        max_permission="safe",
        planner=None,
    ):
        self.tool_intent = tool_intent
        self.tools = tools
        self.file_path_extractor = file_path_extractor
        self.max_permission = max_permission
        self.planner = planner

    def execute(self, user_input):
        tool_name = self.tool_intent.detect(
            user_input
        )

        planning_used = False

        if tool_name is None:
            tool_name = self._plan_tool(
                user_input
            )
            planning_used = tool_name is not None

        if tool_name is None:
            return {
                "used": False,
                "tool_name": None,
                "result": None,
                "context": "",
                "planning_used": planning_used,
            }

        tool = self.tools.get_tool(
            tool_name
        )

        if tool is None:
            return {
                "used": False,
                "tool_name": tool_name,
                "result": {
                    "error": (
                        f"Herramienta desconocida: "
                        f"{tool_name}"
                    )
                },
                "context": "",
                "planning_used": planning_used,
            }

        tool_kwargs = self._build_arguments(
            tool,
            user_input,
        )

        result = self.tools.run(
            tool_name,
            max_permission=self.max_permission,
            **tool_kwargs,
        )

        return {
            "used": True,
            "tool_name": tool_name,
            "result": result,
            "context": self._build_context(
                tool_name,
                result,
            ),
            "planning_used": planning_used,
        }

    def _plan_tool(self, user_input):
        if self.planner is None:
            return None

        try:
            plan = self.planner.plan(
                user_input
            )

        except Exception:
            return None

        if not plan.get(
            "use_tool",
            False,
        ):
            return None

        tool_name = plan.get(
            "tool"
        )

        if not isinstance(
            tool_name,
            str,
        ):
            return None

        if not self.tools.has_tool(
            tool_name
        ):
            return None

        return tool_name

    def _build_arguments(
        self,
        tool,
        user_input,
    ):
        prepare_arguments = getattr(
            tool,
            "prepare_arguments",
            None,
        )

        if prepare_arguments is None:
            return {}

        return prepare_arguments(
            user_input,
            self.file_path_extractor,
        )

    def _build_context(
        self,
        tool_name,
        result,
    ):
        return (
            "\n\n"
            "RESULTADO DE HERRAMIENTA\n"
            "========================\n"
            f"Herramienta: {tool_name}\n"
            f"Resultado:\n{result}\n\n"
            "REGLAS PARA USAR ESTE RESULTADO:\n"
            "- El resultado proviene de una herramienta "
            "real del sistema.\n"
            "- Si el usuario pregunta por ese resultado, "
            "trátalo como fuente primaria.\n"
            "- No atribuyas al archivo, sistema o herramienta "
            "información que no aparezca en el resultado.\n"
            "- Si el resultado no contiene la información "
            "solicitada, dilo claramente.\n"
            "- Puedes utilizar recuerdos y conocimiento "
            "adicional como contexto, pero debes distinguirlos "
            "del contenido de la herramienta.\n"
        )
