from pathlib import Path
import os

from src.rebecca.tools.tool import Tool


class MemoryInfoTool(Tool):
    name = "memory_info"

    description = (
        "Obtiene información sobre la memoria RAM."
    )

    def run(self):
        values = {}

        try:
            with Path(
                "/proc/meminfo"
            ).open(
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as file:
                for line in file:
                    if ":" not in line:
                        continue

                    key, value = line.split(
                        ":",
                        1,
                    )

                    parts = value.strip().split()

                    if not parts:
                        continue

                    try:
                        values[key] = int(
                            parts[0]
                        )
                    except ValueError:
                        continue

        except OSError as error:
            return {
                "error": str(error)
            }

        total_kb = values.get(
            "MemTotal",
            0,
        )

        available_kb = values.get(
            "MemAvailable",
            0,
        )

        used_kb = max(
            total_kb - available_kb,
            0,
        )

        return {
            "total_mb": round(
                total_kb / 1024,
                2,
            ),
            "available_mb": round(
                available_kb / 1024,
                2,
            ),
            "used_mb": round(
                used_kb / 1024,
                2,
            ),
            "logical_cpus": os.cpu_count(),
        }
