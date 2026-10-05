from pathlib import Path
import os
import platform

from src.rebecca.tools.tool import Tool


class CPUInfoTool(Tool):
    name = "cpu_info"

    description = (
        "Obtiene información sobre el procesador."
    )

    permission = "read"

    def run(self):
        return {
            "model": self._get_model(),
            "architecture": platform.machine(),
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
            "Información del procesador:\n\n"
            f"Modelo: "
            f"{result.get('model', 'Desconocido')}\n"
            f"Arquitectura: "
            f"{result.get('architecture', 'Desconocida')}\n"
            f"Núcleos lógicos: "
            f"{result.get('logical_cpus', 'Desconocido')}"
        )

    def _get_model(self):
        cpuinfo = Path(
            "/proc/cpuinfo"
        )

        try:
            with cpuinfo.open(
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as file:
                for line in file:
                    if line.startswith(
                        "model name"
                    ):
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

