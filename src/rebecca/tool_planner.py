import json


class ToolPlanner:
    def __init__(
        self,
        brain,
        tools,
    ):
        self.brain = brain
        self.tools = tools

    def plan(self, user_input):
        available_tools = (
            self.tools.describe_tools()
        )

        tool_descriptions = json.dumps(
            available_tools,
            ensure_ascii=False,
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "Eres el planificador de herramientas "
                    "de Rebecca.\n\n"
                    "Tu trabajo es determinar si una solicitud "
                    "del usuario requiere una herramienta disponible.\n\n"
                    "Herramientas disponibles:\n"
                    f"{tool_descriptions}\n\n"
                    "Responde EXCLUSIVAMENTE con JSON válido.\n"
                    "Si una herramienta es necesaria, responde:\n"
                    '{"use_tool": true, "tool": "nombre"}\n\n'
                    "Si ninguna herramienta es necesaria, responde:\n"
                    '{"use_tool": false, "tool": null}\n\n'
                    "No inventes herramientas.\n"
                    "Solo puedes seleccionar una herramienta "
                    "de la lista proporcionada."
                ),
            },
            {
                "role": "user",
                "content": user_input,
            },
        ]

        response = self.brain.ask(
            messages
        )

        return self._parse_response(
            response
        )

    def _parse_response(self, response):
        try:
            data = json.loads(
                response
            )

        except (
            json.JSONDecodeError,
            TypeError,
        ):
            return {
                "use_tool": False,
                "tool": None,
                "error": "Respuesta inválida del planificador.",
            }

        if not isinstance(
            data,
            dict,
        ):
            return {
                "use_tool": False,
                "tool": None,
                "error": "El planificador no devolvió un objeto.",
            }

        use_tool = data.get(
            "use_tool",
            False,
        )

        tool_name = data.get(
            "tool"
        )

        if not isinstance(
            use_tool,
            bool,
        ):
            use_tool = False

        if use_tool:
            if not isinstance(
                tool_name,
                str,
            ):
                return {
                    "use_tool": False,
                    "tool": None,
                    "error": (
                        "El planificador indicó una herramienta "
                        "sin proporcionar un nombre válido."
                    ),
                }

            if not self.tools.has_tool(
                tool_name
            ):
                return {
                    "use_tool": False,
                    "tool": None,
                    "error": (
                        "El planificador seleccionó una "
                        "herramienta no disponible."
                    ),
                }

            return {
                "use_tool": True,
                "tool": tool_name,
            }

        return {
            "use_tool": False,
            "tool": None,
        }
