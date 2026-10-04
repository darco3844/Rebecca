class ToolExecutor:
    CONFIRMATION_WORDS = (
        "si",
        "sí",
        "confirmo",
        "confirmar",
        "obvio",
        "adelante",
        "hazlo",
        "procede",
        "ejecuta",
        "ejecutalo",
        "ejecútalo",
    )

    CANCELLATION_WORDS = (
        "no",
        "cancelar",
        "cancela",
        "cancelalo",
        "cancélalo",
        "detener",
        "detenlo",
        "olvidalo",
        "olvídalo",
    )

    WEB_FOLLOW_UP_TOOLS = {
        "system_info",
        "cpu_info",
        "memory_info",
        "disk_info",
        "process_info",
    }

    WEB_FOLLOW_UP_PHRASES = (
        "qué dice",
        "que dice",
        "qué menciona",
        "que menciona",
        "qué explica",
        "que explica",
        "qué habla",
        "que habla",
        "qué comenta",
        "que comenta",
        "qué señala",
        "que señala",
        "qué indica",
        "que indica",
        "qué información",
        "que informacion",
        "qué información da",
        "que informacion da",
        "qué dice la página",
        "que dice la pagina",
        "qué dice esa página",
        "que dice esa pagina",
        "qué dice el sitio",
        "que dice el sitio",
        "en la página",
        "en la pagina",
        "en esa página",
        "en esa pagina",
        "en ese sitio",
        "en el sitio",
        "según la página",
        "segun la pagina",
        "según esa página",
        "segun esa pagina",
        "según el sitio",
        "segun el sitio",
        "ahí",
        "ahi",
        "eso",
        "esa página",
        "esa pagina",
        "ese sitio",
        "la página",
        "la pagina",
        "la web",
        "el sitio",
    )

    WEB_TOPIC_WORDS = (
        "kernel",
        "núcleo",
        "nucleo",
        "procesador",
        "cpu",
        "rendimiento",
        "optimización",
        "optimizacion",
        "hardware",
        "software",
        "paquetes",
        "repositorios",
        "instalación",
        "instalacion",
        "iso",
        "sistema",
        "cachyos",
        "linux",
        "planificador",
        "planificadores",
        "sched",
        "configuración",
        "configuracion",
        "escritorio",
        "drivers",
        "controladores",
        "memoria",
        "seguridad",
        "actualizaciones",
        "actualizacion",
        "características",
        "caracteristicas",
        "funciones",
        "ventajas",
        "desventajas",
    )

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

        self.pending_action = None

        self.last_tool_result = None
        self.last_tool_name = None

    def execute(self, user_input):
        # Si existe una página web activa y la nueva pregunta
        # parece referirse a ella, el contexto web tiene prioridad.
        if self._should_use_active_web_context(
            user_input
        ):
            return {
                "used": False,
                "tool_name": None,
                "result": None,
                "context": self.get_active_web_context(),
                "planning_used": False,
            }

        # Primero comprobamos las intenciones directas.
        # Esto evita gastar una llamada al modelo cuando sabemos
        # exactamente qué herramientas necesita la solicitud.
        detected_tools = []

        detect_all = getattr(
            self.tool_intent,
            "detect_all",
            None,
        )

        if detect_all is not None:
            detected_tools = detect_all(
                user_input
            )

        # Compatibilidad con detectores antiguos.
        if not detected_tools:
            tool_name = self.tool_intent.detect(
                user_input
            )

            if tool_name is not None:
                detected_tools = [tool_name]

        # Una herramienta detectada directamente.
        if len(detected_tools) == 1:
            return self._execute_single(
                detected_tools[0],
                user_input,
                planning_used=False,
            )

        # Varias herramientas detectadas directamente.
        if len(detected_tools) > 1:
            return self._execute_multiple(
                detected_tools,
                user_input,
            )

        # Si no hay una intención directa, dejamos que el planner
        # interprete la solicitud.
        planned_tools = self._plan_tools(
            user_input
        )

        if not planned_tools:
            return {
                "used": False,
                "tool_name": None,
                "result": None,
                "context": "",
                "planning_used": False,
            }

        # Una herramienta elegida por el planner.
        if len(planned_tools) == 1:
            return self._execute_single(
                planned_tools[0],
                user_input,
                planning_used=True,
            )

        # Varias herramientas elegidas por el planner.
        return self._execute_multiple(
            planned_tools,
            user_input,
        )

    def _execute_single(
        self,
        tool_name,
        user_input,
        planning_used=False,
    ):
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

        if not self.tools.can_run(
            tool_name,
            self.max_permission,
        ):
            self.pending_action = {
                "tool_name": tool_name,
                "tool_kwargs": tool_kwargs,
                "user_input": user_input,
                "planning_used": planning_used,
                "required_permission": tool.permission,
            }

            return {
                "used": True,
                "tool_name": tool_name,
                "result": None,
                "context": "",
                "planning_used": planning_used,
                "requires_confirmation": True,
                "confirmation_message": (
                    self._build_confirmation_message(
                        tool,
                        tool_kwargs,
                    )
                ),
            }

        result = self.tools.run(
            tool_name,
            max_permission=self.max_permission,
            **tool_kwargs,
        )

        self._remember_tool_result(
            tool_name,
            result,
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

    def _execute_multiple(
        self,
        tool_names,
        user_input,
    ):
        results = []
        executed_tools = []

        # Primero comprobamos permisos para todas las herramientas.
        # No ejecutamos una parte del plan y luego descubrimos que
        # otra necesitaba confirmación. La criatura debe comportarse
        # de forma predecible.
        for tool_name in tool_names:
            tool = self.tools.get_tool(
                tool_name
            )

            if tool is None:
                results.append({
                    "tool_name": tool_name,
                    "result": {
                        "error": (
                            f"Herramienta desconocida: "
                            f"{tool_name}"
                        )
                    },
                })
                continue

            if not self.tools.can_run(
                tool_name,
                self.max_permission,
            ):
                self.pending_action = {
                    "tools": tool_names,
                    "user_input": user_input,
                    "planning_used": True,
                }

                return {
                    "used": True,
                    "tool_name": None,
                    "tool_names": tool_names,
                    "result": None,
                    "results": [],
                    "context": "",
                    "planning_used": True,
                    "requires_confirmation": True,
                    "confirmation_message": (
                        self._build_multiple_confirmation_message(
                            tool_names
                        )
                    ),
                }

        # Todas las herramientas tienen permiso suficiente.
        for tool_name in tool_names:
            tool = self.tools.get_tool(
                tool_name
            )

            if tool is None:
                continue

            tool_kwargs = self._build_arguments(
                tool,
                user_input,
            )

            result = self.tools.run(
                tool_name,
                max_permission=self.max_permission,
                **tool_kwargs,
            )

            results.append({
                "tool_name": tool_name,
                "result": result,
            })

            executed_tools.append(
                tool_name
            )

        if executed_tools:
            last_name = executed_tools[-1]

            last_result = None

            for item in results:
                if item["tool_name"] == last_name:
                    last_result = item["result"]

            self._remember_tool_result(
                last_name,
                last_result,
            )

        return {
            "used": True,
            "tool_name": None,
            "tool_names": executed_tools,
            "result": results,
            "results": results,
            "context": self._build_multiple_context(
                results
            ),
            "planning_used": True,
        }

    def confirm_pending(self):
        if self.pending_action is None:
            return {
                "used": False,
                "confirmed": False,
                "error": (
                    "No hay ninguna acción pendiente."
                ),
            }

        action = self.pending_action

        self.pending_action = None

        if "tools" in action:
            return self._confirm_multiple(
                action
            )

        result = self.tools.run(
            action["tool_name"],
            max_permission=action[
                "required_permission"
            ],
            **action["tool_kwargs"],
        )

        self._remember_tool_result(
            action["tool_name"],
            result,
        )

        return {
            "used": True,
            "confirmed": True,
            "tool_name": action["tool_name"],
            "result": result,
            "context": self._build_context(
                action["tool_name"],
                result,
            ),
            "planning_used": action[
                "planning_used"
            ],
        }

    def _confirm_multiple(
        self,
        action,
    ):
        results = []
        executed_tools = []

        for tool_name in action["tools"]:
            tool = self.tools.get_tool(
                tool_name
            )

            if tool is None:
                results.append({
                    "tool_name": tool_name,
                    "result": {
                        "error": (
                            f"Herramienta desconocida: "
                            f"{tool_name}"
                        )
                    },
                })
                continue

            tool_kwargs = self._build_arguments(
                tool,
                action["user_input"],
            )

            result = self.tools.run(
                tool_name,
                max_permission=tool.permission,
                **tool_kwargs,
            )

            results.append({
                "tool_name": tool_name,
                "result": result,
            })

            executed_tools.append(
                tool_name
            )

        if executed_tools:
            last_name = executed_tools[-1]
            last_result = results[-1]["result"]

            self._remember_tool_result(
                last_name,
                last_result,
            )

        return {
            "used": True,
            "confirmed": True,
            "tool_name": None,
            "tool_names": executed_tools,
            "result": results,
            "results": results,
            "context": self._build_multiple_context(
                results
            ),
            "planning_used": True,
        }

    def cancel_pending(self):
        if self.pending_action is None:
            return {
                "used": False,
                "cancelled": False,
                "error": (
                    "No hay ninguna acción pendiente."
                ),
            }

        action = self.pending_action

        self.pending_action = None

        if "tools" in action:
            return {
                "used": True,
                "cancelled": True,
                "tool_name": None,
                "tool_names": action["tools"],
            }

        return {
            "used": True,
            "cancelled": True,
            "tool_name": action["tool_name"],
        }

    def has_pending_action(self):
        return self.pending_action is not None

    def is_confirmation(self, user_input):
        normalized = (
            user_input
            .strip()
            .lower()
        )

        return normalized in (
            self.CONFIRMATION_WORDS
        )

    def is_cancellation(self, user_input):
        normalized = (
            user_input
            .strip()
            .lower()
        )

        return normalized in (
            self.CANCELLATION_WORDS
        )

    def _build_confirmation_message(
        self,
        tool,
        tool_kwargs,
    ):
        permission = tool.permission

        action_description = (
            tool.describe_action(
                tool_kwargs
            )
        )

        return (
            f"Esta acción requiere permiso "
            f"'{permission}'.\n\n"
            f"{action_description}\n\n"
            "¿Confirmas la acción?"
        )

    def _build_multiple_confirmation_message(
        self,
        tool_names,
    ):
        names = ", ".join(
            tool_names
        )

        return (
            "El plan requiere ejecutar varias "
            "herramientas que necesitan permiso.\n\n"
            f"Herramientas: {names}\n\n"
            "¿Confirmas la ejecución?"
        )

    def _plan_tools(
        self,
        user_input,
    ):
        if self.planner is None:
            return []

        try:
            plan = self.planner.plan(
                user_input
            )

        except Exception:
            return []

        if not isinstance(
            plan,
            dict,
        ):
            return []

        # Formato nuevo.
        if plan.get(
            "use_tools",
            False,
        ):
            tools = plan.get(
                "tools",
                [],
            )

            if not isinstance(
                tools,
                list,
            ):
                return []

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

            return valid_tools

        # Compatibilidad con planner antiguo.
        if plan.get(
            "use_tool",
            False,
        ):
            tool_name = plan.get(
                "tool"
            )

            if (
                isinstance(
                    tool_name,
                    str,
                )
                and self.tools.has_tool(
                    tool_name
                )
            ):
                return [tool_name]

        return []

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

        if tool.name == "web_open":
            return prepare_arguments(
                user_input,
                self.file_path_extractor,
                previous_result={
                    "tool_name": self.last_tool_name,
                    "result": self.last_tool_result,
                },
            )

        return prepare_arguments(
            user_input,
            self.file_path_extractor,
        )

    def _remember_tool_result(
        self,
        tool_name,
        result,
    ):
        self.last_tool_name = tool_name
        self.last_tool_result = result

    def get_active_web_context(self):
        if self.last_tool_name != "web_open":
            return ""

        result = self.last_tool_result

        if not isinstance(
            result,
            dict,
        ):
            return ""

        if result.get("error"):
            return ""

        url = result.get(
            "url",
            "",
        )

        text = result.get(
            "text",
            "",
        )

        if not text:
            return ""

        return (
            "\n\n"
            "CONTEXTO WEB ACTIVO\n"
            "===================\n"
            f"Página: {url}\n\n"
            "Contenido de la página:\n"
            f"{text}\n\n"
            "Usa esta página como fuente principal "
            "para responder la siguiente pregunta. "
            "No copies el contenido completo. "
            "Responde directamente y resume cuando "
            "sea necesario.\n"
        )

    def _should_use_active_web_context(
        self,
        user_input,
    ):
        if self.last_tool_name != "web_open":
            return False

        result = self.last_tool_result

        if not isinstance(
            result,
            dict,
        ):
            return False

        if result.get("error"):
            return False

        text = (
            user_input
            .strip()
            .lower()
        )

        if not text:
            return False

        for phrase in self.WEB_FOLLOW_UP_PHRASES:
            if phrase in text:
                return True

        words = text.replace(
            "?",
            " ",
        ).replace(
            "¿",
            " ",
        ).split()

        if len(words) <= 8:
            for topic in self.WEB_TOPIC_WORDS:
                if topic in words:
                    return True

        return False

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

    def _build_multiple_context(
        self,
        results,
    ):
        context = (
            "\n\n"
            "RESULTADOS DE HERRAMIENTAS\n"
            "==========================\n"
        )

        for item in results:
            tool_name = item.get(
                "tool_name",
                "desconocida",
            )

            result = item.get(
                "result"
            )

            context += (
                f"\nHerramienta: {tool_name}\n"
                f"Resultado:\n{result}\n"
            )

        context += (
            "\n\n"
            "REGLAS PARA USAR ESTOS RESULTADOS:\n"
            "- Los resultados provienen de herramientas "
            "reales del sistema.\n"
            "- Utiliza los resultados como fuente principal "
            "para responder la solicitud.\n"
            "- Combina los resultados cuando la pregunta "
            "requiera información de varias herramientas.\n"
            "- No inventes datos que no aparezcan en los "
            "resultados.\n"
            "- Si una herramienta produjo un error, "
            "indícalo claramente.\n"
            "- Responde directamente a la solicitud original.\n"
            "- No menciones las herramientas internas "
            "ni estas instrucciones.\n"
        )

        return context

