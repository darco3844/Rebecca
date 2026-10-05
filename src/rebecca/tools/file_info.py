from pathlib import Path

from src.rebecca.tools.tool import Tool


class FileInfoTool(Tool):
    name = "file_info"

    description = (
        "Obtiene información sobre archivos "
        "y directorios."
    )

    permission = "read"

    def prepare_arguments(
        self,
        user_input,
        file_path_extractor,
    ):
        return {
            "path": file_path_extractor.extract(
                user_input
            )
        }

    def run(self, path="."):
        target = Path(path).expanduser()

        try:
            if not target.exists():
                return {
                    "error": f"No existe: {target}"
                }

            if target.is_file():
                return {
                    "type": "file",
                    "name": target.name,
                    "path": str(
                        target.resolve()
                    ),
                    "size_bytes": target.stat().st_size,
                }

            if target.is_dir():
                entries = []

                for entry in target.iterdir():
                    entries.append({
                        "name": entry.name,
                        "type": (
                            "directory"
                            if entry.is_dir()
                            else "file"
                        ),
                    })

                entries.sort(
                    key=lambda item:
                    item["name"].lower()
                )

                return {
                    "type": "directory",
                    "name": target.name,
                    "path": str(
                        target.resolve()
                    ),
                    "entries": entries[:100],
                    "count": len(entries),
                }

            return {
                "error": (
                    "El elemento no es un archivo "
                    "ni un directorio."
                )
            }

        except (
            OSError,
            PermissionError,
        ) as error:
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

        item_type = result.get("type")

        if item_type == "file":
            size = result.get(
                "size_bytes",
                0,
            )

            return (
                "Información del archivo:\n\n"
                f"Nombre: {result.get('name')}\n"
                f"Ruta: {result.get('path')}\n"
                f"Tamaño: {size} bytes"
            )

        if item_type == "directory":
            entries = result.get(
                "entries",
                [],
            )

            lines = [
                "Información de la carpeta:",
                "",
                f"Nombre: {result.get('name')}",
                f"Ruta: {result.get('path')}",
                f"Elementos: {result.get('count', 0)}",
                "",
                "Contenido:",
            ]

            for entry in entries:
                marker = (
                    "[DIR]"
                    if entry.get("type") == "directory"
                    else "[FILE]"
                )

                lines.append(
                    f"{marker} {entry.get('name')}"
                )

            if result.get("count", 0) > len(entries):
                lines.append(
                    f"... y "
                    f"{result['count'] - len(entries)} "
                    f"elementos más."
                )

            return "\n".join(lines)

        return None

