from pathlib import Path
import os
import platform

from src.rebecca.tools.tool import Tool


class CPUInfoTool(Tool):
    name = "cpu_info"

    description = (
        "Obtiene información sobre el procesador."
    )

    def run(self):
        return {
            "model": self._get_model(),
            "architecture": platform.machine(),
            "logical_cpus": os.cpu_count(),
        }

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
