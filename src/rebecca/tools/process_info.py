from pathlib import Path

from src.rebecca.tools.tool import Tool


class ProcessInfoTool(Tool):
    name = "process_info"

    description = (
        "Obtiene información básica sobre "
        "los procesos activos."
    )

    permission = "read"

    def run(self):
        processes = []

        proc_path = Path("/proc")

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

    def format_result(
        self,
        result,
        user_input="",
    ):
        if not isinstance(result, dict):
            return None

        if result.get("error"):
            return f"Error: {result['error']}"

        processes = result.get(
            "processes",
            [],
        )

        lines = [
            "Procesos activos:",
            "",
            f"Procesos detectados: "
            f"{result.get('count', 0)}",
            "",
        ]

        for process in processes:
            lines.append(
                f"{process.get('pid')}: "
                f"{process.get('name')}"
            )

        if result.get("count", 0) > len(processes):
            lines.extend([
                "",
                f"... mostrando los primeros "
                f"{len(processes)} procesos.",
            ])

        return "\n".join(lines)

