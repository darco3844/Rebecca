from pathlib import Path

from src.rebecca.tools.tool import Tool


class FileInfoTool(Tool):
    name = "file_info"

    description = (
        "Obtiene información sobre archivos y directorios."
    )

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
                    "path": str(target.resolve()),
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
                    key=lambda item: item["name"].lower()
                )

                return {
                    "type": "directory",
                    "name": target.name,
                    "path": str(target.resolve()),
                    "entries": entries[:100],
                    "count": len(entries),
                }

            return {
                "error": (
                    "El elemento no es un archivo "
                    "ni un directorio."
                )
            }

        except (OSError, PermissionError) as error:
            return {
                "error": str(error)
            }
