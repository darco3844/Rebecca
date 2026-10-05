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

    permission = "read"

    def run(self):
        return {
            "os": platform.system(),
            "distribution": self._get_distribution(),
            "kernel": platform.release(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "cpu": self._get_cpu_model(),
            "logical_cpus": os.cpu_count(),
        }

    def format_result(
        self,
        result,
        user_input="",
    ):
        if not isinstance(result, dict):
            return None

        if result.get("error"):
            return f"Error: {result['error']}"

        return (
            "Información del sistema:\n\n"
            f"Sistema operativo: "
            f"{result.get('distribution', 'Desconocido')}\n"
            f"Kernel: {result.get('kernel', 'Desconocido')}\n"
            f"Arquitectura: "
            f"{result.get('architecture', 'Desconocida')}\n"
            f"Procesador: "
            f"{result.get('cpu', 'Desconocido')}\n"
            f"Núcleos lógicos: "
            f"{result.get('logical_cpus', 'Desconocido')}\n"
            f"Equipo: "
            f"{result.get('hostname', 'Desconocido')}"
        )

    def _get_cpu_model(self):
        cpuinfo = Path("/proc/cpuinfo")

        try:
            with cpuinfo.open(
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as file:
                for line in file:
                    if line.startswith("model name"):
                        return line.split(
                            ":",
                            1,
                        )[1].strip()

        except (
            OSError,
            IndexError,
        ):
            pass

        processor = platform.processor()

        if processor:
            return processor

        return "Desconocido"

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

                    data[key] = value.strip('"')

            return data.get(
                "PRETTY_NAME",
                data.get(
                    "NAME",
                    "Desconocido",
                ),
            )

        except OSError:
            return "Desconocido"

