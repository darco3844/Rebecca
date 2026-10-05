import json
from pathlib import Path


class PluginConfig:
    def __init__(
        self,
        config_path="data/config/plugins.json",
    ):
        self.config_path = Path(
            config_path
        )

        self.config_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.config = self._load()

    def _load(self):
        if not self.config_path.exists():
            return {
                "plugins": {}
            }

        try:
            with self.config_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

        except (
            OSError,
            json.JSONDecodeError,
        ):
            return {
                "plugins": {}
            }

        if not isinstance(
            data,
            dict,
        ):
            return {
                "plugins": {}
            }

        if not isinstance(
            data.get("plugins"),
            dict,
        ):
            data["plugins"] = {}

        return data

    def save(self):
        with self.config_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self.config,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def list_plugins(self):
        return list(
            self.config.get(
                "plugins",
                {},
            ).keys()
        )

    def is_enabled(
        self,
        plugin_name,
    ):
        plugin = self.config[
            "plugins"
        ].get(
            plugin_name
        )

        if plugin is None:
            return False

        return bool(
            plugin.get(
                "enabled",
                False,
            )
        )

    def set_enabled(
        self,
        plugin_name,
        enabled,
    ):
        plugin = self.config[
            "plugins"
        ].setdefault(
            plugin_name,
            {},
        )

        plugin["enabled"] = bool(
            enabled
        )

        self.save()

    def get_permission(
        self,
        plugin_name,
        tool_name,
        default="read",
    ):
        plugin = self.config[
            "plugins"
        ].get(
            plugin_name,
            {},
        )

        permissions = plugin.get(
            "permissions",
            {},
        )

        return permissions.get(
            tool_name,
            default,
        )

    def set_permission(
        self,
        plugin_name,
        tool_name,
        permission,
    ):
        plugin = self.config[
            "plugins"
        ].setdefault(
            plugin_name,
            {},
        )

        permissions = plugin.setdefault(
            "permissions",
            {},
        )

        permissions[
            tool_name
        ] = permission

        self.save()

    def get_plugin_config(
        self,
        plugin_name,
    ):
        return self.config[
            "plugins"
        ].get(
            plugin_name,
            {},
        )
