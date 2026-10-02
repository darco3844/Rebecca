from src.rebecca.tools.catalog import (
    TOOL_CATALOG,
)


class ToolManager:
    PERMISSIONS = {
        "read": 0,
        "safe": 1,
        "sensitive": 2,
        "critical": 3,
    }

    def __init__(
        self,
        catalog=None,
    ):
        self.tools = {}

        if catalog is None:
            catalog = TOOL_CATALOG

        self._load_catalog(
            catalog
        )

    def _load_catalog(
        self,
        catalog,
    ):
        for entry in catalog:
            tool_class = entry["tool"]
            permission = entry.get(
                "permission"
            )

            self.register(
                tool_class(),
                permission=permission,
            )

    def register(
        self,
        tool,
        permission=None,
    ):
        required_methods = [
            "run",
            "prepare_arguments",
            "describe",
        ]

        for method in required_methods:
            if not callable(
                getattr(tool, method, None)
            ):
                raise TypeError(
                    f"La herramienta "
                    f"'{getattr(tool, 'name', '?')}' "
                    f"no implementa "
                    f"'{method}()'."
                )

        if not getattr(
            tool,
            "name",
            None,
        ):
            raise ValueError(
                "La herramienta debe tener un nombre."
            )

        if not getattr(
            tool,
            "description",
            None,
        ):
            raise ValueError(
                f"La herramienta '{tool.name}' "
                "debe tener una descripción."
            )

        if permission is not None:
            tool.permission = permission

        if tool.permission not in self.PERMISSIONS:
            raise ValueError(
                f"Permiso desconocido: "
                f"{tool.permission}"
            )

        if tool.name in self.tools:
            raise ValueError(
                f"La herramienta "
                f"'{tool.name}' ya está registrada."
            )

        self.tools[tool.name] = tool

    def has_tool(self, name):
        return name in self.tools

    def get_tool(self, name):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.keys())

    def describe_tools(self):
        return [
            tool.describe()
            for tool in self.tools.values()
        ]

    def can_run(
        self,
        name,
        max_permission="read",
    ):
        tool = self.get_tool(name)

        if tool is None:
            return False

        tool_level = self.PERMISSIONS.get(
            tool.permission,
            99,
        )

        allowed_level = self.PERMISSIONS.get(
            max_permission,
            0,
        )

        return tool_level <= allowed_level

    def run(
        self,
        name,
        max_permission="read",
        **kwargs,
    ):
        tool = self.get_tool(name)

        if tool is None:
            return {
                "error": (
                    f"Herramienta desconocida: {name}"
                )
            }

        if not self.can_run(
            name,
            max_permission,
        ):
            return {
                "error": (
                    f"La herramienta '{name}' requiere "
                    f"permiso '{tool.permission}'."
                ),
                "permission_required": tool.permission,
            }

        try:
            return tool.run(**kwargs)

        except Exception as error:
            return {
                "error": str(error)
            }
