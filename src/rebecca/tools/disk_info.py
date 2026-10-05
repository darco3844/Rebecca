import shutil

from src.rebecca.tools.tool import Tool


class DiskInfoTool(Tool):
    name = "disk_info"

    description = (
        "Obtiene información sobre el espacio "
        "del almacenamiento."
    )

    permission = "read"

    def run(self):
        try:
            total, used, free = shutil.disk_usage(
                "/"
            )

            total_gb = total / (
                1024 ** 3
            )

            used_gb = used / (
                1024 ** 3
            )

            free_gb = free / (
                1024 ** 3
            )

            used_percent = (
                (used / total) * 100
                if total
                else 0
            )

            return {
                "total_gb": round(
                    total_gb,
                    2,
                ),
                "used_gb": round(
                    used_gb,
                    2,
                ),
                "free_gb": round(
                    free_gb,
                    2,
                ),
                "used_percent": round(
                    used_percent,
                    2,
                ),
            }

        except OSError as error:
            return {
                "error": str(error)
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
            "Espacio de almacenamiento:\n\n"
            f"Total: "
            f"{result.get('total_gb', 0):.2f} GB\n"
            f"Usado: "
            f"{result.get('used_gb', 0):.2f} GB "
            f"({result.get('used_percent', 0):.2f} %)\n"
            f"Libre: "
            f"{result.get('free_gb', 0):.2f} GB"
        )

