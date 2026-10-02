import importlib


class PluginManager:
    def __init__(
        self,
        tool_manager,
        config=None,
    ):
        self.tool_manager = tool_manager
        self.config = config
        self.plugins = {}
        self.plugin_tools = {}

    def register(self, plugin):
        if not getattr(
            plugin,
            "name",
            None,
        ):
            raise ValueError(
                "El plugin debe tener un nombre."
            )

        if plugin.name in self.plugins:
            raise ValueError(
                f"El plugin '{plugin.name}' "
                "ya está registrado."
            )

        if (
            self.config is not None
            and not self.config.is_enabled(
                plugin.name
            )
        ):
            return False

        tools = plugin.get_tools()

        registered_tools = []

        try:
            for tool in tools:
                permission = self._get_permission(
                    plugin.name,
                    tool.name,
                    tool.permission,
                )

                self.tool_manager.register(
                    tool,
                    permission=permission,
                )

                registered_tools.append(
                    tool.name
                )

            plugin.initialize()

        except Exception:
            for tool_name in registered_tools:
                self.tool_manager.unregister(
                    tool_name
                )

            raise

        self.plugins[plugin.name] = plugin

        self.plugin_tools[
            plugin.name
        ] = registered_tools

        return True

    def unregister(self, name):
        plugin = self.plugins.get(name)

        if plugin is None:
            return False

        plugin.shutdown()

        tool_names = self.plugin_tools.get(
            name,
            [],
        )

        for tool_name in tool_names:
            self.tool_manager.unregister(
                tool_name
            )

        del self.plugins[name]

        self.plugin_tools.pop(
            name,
            None,
        )

        return True

    def has_plugin(self, name):
        return name in self.plugins

    def get_plugin(self, name):
        return self.plugins.get(name)

    def list_plugins(self):
        return list(
            self.plugins.keys()
        )

    def describe_plugins(self):
        return [
            plugin.describe()
            for plugin in self.plugins.values()
        ]

    def load_module(self, module_name):
        module = importlib.import_module(
            module_name
        )

        plugin_class = getattr(
            module,
            "PLUGIN_CLASS",
            None,
        )

        if plugin_class is None:
            raise ValueError(
                f"El módulo '{module_name}' "
                "no define PLUGIN_CLASS."
            )

        plugin = plugin_class()

        return self.register(
            plugin
        )

    def _get_permission(
        self,
        plugin_name,
        tool_name,
        default,
    ):
        if self.config is None:
            return default

        return self.config.get_permission(
            plugin_name,
            tool_name,
            default=default,
        )
