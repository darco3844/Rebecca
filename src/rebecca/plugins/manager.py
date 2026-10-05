import importlib


class PluginManager:
    def __init__(
        self,
        tool_manager,
        config=None,
        secrets=None,
        catalog=None,
    ):
        self.tool_manager = tool_manager
        self.config = config
        self.secrets = secrets

        self.plugins = {}
        self.plugin_tools = {}
        self.plugin_modules = {}

        if catalog is None:
            from src.rebecca.plugins.catalog import PLUGIN_CATALOG
            catalog = PLUGIN_CATALOG

        self.plugin_catalog = self._normalize_catalog(catalog)

    def _normalize_catalog(self, catalog):
        normalized = {}
        for entry in catalog:
            name = entry.get("name")
            module = entry.get("module")
            if not name:
                raise ValueError("Cada plugin del catálogo debe tener un nombre.")
            if not module:
                raise ValueError(f"El plugin '{name}' debe tener un módulo.")
            if name in normalized:
                raise ValueError(f"El plugin '{name}' está duplicado en el catálogo.")
            normalized[name] = module
        return normalized

    def register(self, plugin, module_name=None):
        if not getattr(plugin, "name", None):
            raise ValueError("El plugin debe tener un nombre.")
        if plugin.name in self.plugins:
            raise ValueError(f"El plugin '{plugin.name}' ya está registrado.")
        if self.config is not None and not self.config.is_enabled(plugin.name):
            return False

        self._inject_dependencies(plugin)
        tools = plugin.get_tools()
        registered_tools = []

        try:
            for tool in tools:
                permission = self._get_permission(
                    plugin.name,
                    tool.name,
                    tool.permission,
                )
                self.tool_manager.register(tool, permission=permission)
                registered_tools.append(tool.name)
            plugin.initialize()
        except Exception:
            for tool_name in registered_tools:
                self.tool_manager.unregister(tool_name)
            raise

        self.plugins[plugin.name] = plugin
        self.plugin_tools[plugin.name] = registered_tools

        if module_name is not None:
            self.plugin_modules[plugin.name] = module_name

        return True

    def unregister(self, name):
        plugin = self.plugins.get(name)
        if plugin is None:
            return False

        plugin.shutdown()
        for tool_name in self.plugin_tools.get(name, []):
            self.tool_manager.unregister(tool_name)

        del self.plugins[name]
        self.plugin_tools.pop(name, None)
        return True

    def has_plugin(self, name):
        return name in self.plugins

    def get_plugin(self, name):
        return self.plugins.get(name)

    def list_plugins(self):
        return list(self.plugins.keys())

    def list_catalog_plugins(self):
        return list(self.plugin_catalog.keys())

    def describe_plugins(self):
        return [plugin.describe() for plugin in self.plugins.values()]

    def describe_plugin(self, name):
        plugin = self.get_plugin(name)
        if plugin is None:
            return None
        return plugin.describe()

    def get_plugin_tools(self, name):
        return list(self.plugin_tools.get(name, []))

    def get_plugin_module(self, name):
        return self.plugin_modules.get(
            name,
            self.plugin_catalog.get(name),
        )

    def is_enabled(self, name):
        if self.config is None:
            return self.has_plugin(name)
        return self.config.is_enabled(name)

    def get_plugin_state(self, name):
        plugin = self.get_plugin(name)
        module = self.get_plugin_module(name)

        if plugin is None:
            return {
                "name": name,
                "enabled": self.is_enabled(name),
                "loaded": False,
                "module": module,
                "tools": [],
            }

        description = plugin.describe()
        return {
            "name": description.get("name", name),
            "description": description.get("description", ""),
            "version": description.get("version", ""),
            "enabled": self.is_enabled(name),
            "loaded": True,
            "module": module,
            "tools": description.get("tools", []),
        }

    def describe_plugin_states(self):
        names = set(self.plugin_catalog.keys())
        names.update(self.plugins.keys())
        if self.config is not None:
            names.update(self.config.list_plugins())
        return [self.get_plugin_state(name) for name in sorted(names)]

    def load_plugin(self, name):
        if self.has_plugin(name):
            return self.get_plugin_state(name)

        module_name = self.plugin_catalog.get(name)
        if module_name is None:
            return {
                "name": name,
                "enabled": self.is_enabled(name),
                "loaded": False,
                "module": None,
                "tools": [],
                "error": "El plugin no existe en el catálogo.",
            }

        if self.config is not None and not self.config.is_enabled(name):
            return {
                "name": name,
                "enabled": False,
                "loaded": False,
                "module": module_name,
                "tools": [],
                "error": "El plugin está deshabilitado.",
            }

        self.load_module(module_name)
        return self.get_plugin_state(name)

    def load_enabled_plugins(self):
        results = []
        for name in self.plugin_catalog:
            if self.is_enabled(name):
                results.append(self.load_plugin(name))
        return results

    def set_enabled(self, name, enabled):
        if self.config is None:
            raise RuntimeError(
                "PluginManager necesita PluginConfig para cambiar el estado de un plugin."
            )

        if name not in self.plugin_catalog:
            return {
                "name": name,
                "enabled": False,
                "loaded": False,
                "module": None,
                "tools": [],
                "error": "El plugin no existe en el catálogo.",
            }

        self.config.set_enabled(name, enabled)

        if not enabled:
            if self.has_plugin(name):
                self.unregister(name)
            return self.get_plugin_state(name)

        return self.load_plugin(name)

    def load_module(self, module_name):
        module = importlib.import_module(module_name)
        plugin_class = getattr(module, "PLUGIN_CLASS", None)
        if plugin_class is None:
            raise ValueError(
                f"El módulo '{module_name}' no define PLUGIN_CLASS."
            )

        plugin = plugin_class()
        plugin_name = getattr(plugin, "name", None)
        if plugin_name is None:
            raise ValueError(
                f"El módulo '{module_name}' creó un plugin sin nombre."
            )

        catalog_module = self.plugin_catalog.get(plugin_name)
        if catalog_module is not None and catalog_module != module_name:
            raise ValueError(
                f"El plugin '{plugin_name}' no coincide con el módulo registrado en el catálogo."
            )

        self.plugin_modules[plugin_name] = module_name
        return self.register(plugin, module_name=module_name)

    def _inject_dependencies(self, plugin):
        plugin.config = self.config
        plugin.secrets = self.secrets

    def _get_permission(self, plugin_name, tool_name, default):
        if self.config is None:
            return default
        return self.config.get_permission(
            plugin_name,
            tool_name,
            default=default,
        )
