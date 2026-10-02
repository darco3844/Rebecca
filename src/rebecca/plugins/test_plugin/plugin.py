from src.rebecca.plugins.plugin import Plugin
from src.rebecca.tools.tool import Tool


class PluginTestTool(Tool):
    name = "plugin_test"

    description = (
        "Herramienta de prueba para verificar "
        "que el sistema de plugins funciona."
    )

    permission = "read"

    def run(self):
        return {
            "status": "ok",
            "message": (
                "El sistema de plugins de Rebecca "
                "está funcionando."
            ),
        }


class TestPlugin(Plugin):
    name = "test_plugin"

    description = (
        "Plugin de prueba del sistema de plugins."
    )

    version = "1.0.0"

    def get_tools(self):
        return [
            PluginTestTool(),
        ]


PLUGIN_CLASS = TestPlugin
