import json
import re


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

                    "Tu trabajo es determinar qué herramientas "
                    "disponibles necesita una solicitud del usuario.\n\n"

                    "IMPORTANTE:\n"
                    "- Las intenciones obvias ya son detectadas "
                    "antes de llegar a ti.\n"
                    "- Solo debes decidir cuando la solicitud "
                    "es ambigua o contiene varias tareas.\n"
                    "- No inventes herramientas.\n"
                    "- Solo puedes seleccionar herramientas "
                    "de la lista proporcionada.\n"
                    "- Puedes seleccionar varias herramientas "
                    "cuando la solicitud necesite varias tareas "
                    "independientes.\n"
                    "- No selecciones una herramienta solamente "
                    "porque una palabra coincida con su descripción.\n"
                    "- Si la solicitud es conversación normal, "
                    "información general o una respuesta que no "
                    "requiere herramientas, devuelve false.\n\n"

                    "EJEMPLO:\n"
                    "Usuario: "
                    "\"Dime cuánto espacio tengo y qué procesador tengo.\"\n"
                    "Respuesta:\n"
                    '{"use_tools": true, '
                    '"tools": ["disk_info", "cpu_info"]}\n\n'

                    "Si solo se necesita una herramienta:\n"
                    '{"use_tools": true, '
                    '"tools": ["nombre"]}\n\n'

                    "Si no se necesita ninguna:\n"
                    '{"use_tools": false, "tools": []}\n\n'

                    "Herramientas disponibles:\n"
                    f"{tool_descriptions}\n\n"

                    "Responde EXCLUSIVAMENTE con JSON válido."
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

    def _parse_response(
        self,
        response,
    ):
        if not isinstance(
            response,
            str,
        ):
            return {
                "use_tools": False,
                "tools": [],
                "error": (
                    "Respuesta inválida del planificador."
                ),
            }

        response = response.strip()

        try:
            data = json.loads(
                response
            )

        except json.JSONDecodeError:
            data = self._extract_json_object(
                response
            )

        if data is None:
            return {
                "use_tools": False,
                "tools": [],
                "error": (
                    "Respuesta inválida del planificador."
                ),
            }

        if not isinstance(
            data,
            dict,
        ):
            return {
                "use_tools": False,
                "tools": [],
                "error": (
                    "El planificador no devolvió "
                    "un objeto."
                ),
            }

        use_tools = data.get(
            "use_tools"
        )

        tools = data.get(
            "tools"
        )

        # Compatibilidad con el formato anterior.
        if use_tools is None:
            use_tool = data.get(
                "use_tool",
                False,
            )

            old_tool = data.get(
                "tool"
            )

            if (
                isinstance(
                    use_tool,
                    bool,
                )
                and use_tool
                and isinstance(
                    old_tool,
                    str,
                )
            ):
                use_tools = True
                tools = [old_tool]

            else:
                use_tools = False
                tools = []

        if not isinstance(
            use_tools,
            bool,
        ):
            use_tools = False

        if not isinstance(
            tools,
            list,
        ):
            tools = []

        valid_tools = []

        for tool_name in tools:
            if not isinstance(
                tool_name,
                str,
            ):
                continue

            tool_name = tool_name.strip()

            if not tool_name:
                continue

            if not self.tools.has_tool(
                tool_name
            ):
                continue

            if tool_name not in valid_tools:
                valid_tools.append(
                    tool_name
                )

        if not valid_tools:
            return {
                "use_tools": False,
                "tools": [],
            }

        return {
            "use_tools": True,
            "tools": valid_tools,
        }

    def _extract_json_object(
        self,
        response,
    ):
        fenced_match = re.search(
            r"```(?:json)?\s*(\{.*?\})\s*```",
            response,
            re.IGNORECASE | re.DOTALL,
        )

        if fenced_match:
            candidate = fenced_match.group(
                1
            )

            try:
                return json.loads(
                    candidate
                )

            except json.JSONDecodeError:
                pass

        start = response.find(
            "{"
        )

        if start == -1:
            return None

        end = response.rfind(
            "}"
        )

        if end == -1 or end <= start:
            return None

        candidate = response[
            start:end + 1
        ]

        try:
            return json.loads(
                candidate
            )

        except json.JSONDecodeError:
            return None

