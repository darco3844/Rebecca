from pathlib import Path

from src.rebecca.tools.tool import Tool


class ProcessInfoTool(Tool):
    name = "process_info"

    description = (
        "Obtiene información básica sobre "
        "los procesos activos."
    )

    def run(self):
        processes = []

        proc_path = Path(
            "/proc"
        )

        try:
            entries = list(
                proc_path.iterdir()
            )

            for entry in entries:
                if not entry.name.isdigit():
                    continue

                pid = int(entry.name)

                try:
                    name = (
                        entry / "comm"
                    ).read_text(
                        encoding="utf-8",
                        errors="ignore",
                    ).strip()

                except OSError:
                    continue

                processes.append({
                    "pid": pid,
                    "name": name,
                })

        except OSError as error:
            return {
                "error": str(error)
            }

        processes.sort(
            key=lambda item: item["pid"]
        )

        return {
            "processes": processes[:50],
            "count": len(processes),
        }
