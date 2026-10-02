from pathlib import Path
import platform
import os

from src.rebecca.tools.tool import Tool


class SystemInfoTool(Tool):
    name = "system_info"

    description = (
        "Obtiene información básica del sistema "
        "operativo y hardware."
    )

    def run(self):
        return {
            "os": platform.system(),
            "distribution": self._get_distribution(),
            "kernel": platform.release(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "cpu": platform.processor(),
            "logical_cpus": os.cpu_count(),
        }

    def _get_distribution(self):
        os_release = Path(
            "/etc/os-release"
        )

        try:
            data = {}

            with os_release.open(
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as file:
                for line in file:
                    if "=" not in line:
                        continue

                    key, value = line.strip().split(
                        "=",
                        1,
                    )

                    data[key] = value.strip(
                        '"'
                    )

            return data.get(
                "PRETTY_NAME",
                data.get("NAME", "Desconocido"),
            )

        except OSError:
            return "Desconocido"
