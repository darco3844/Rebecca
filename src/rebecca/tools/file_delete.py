from pathlib import Path

from src.rebecca.tools.tool import Tool


class FileDeleteTool(Tool):
    name = "file_delete"

    description = (
        "Elimina un archivo existente dentro "
        "del proyecto Rebecca."
    )

    permission = "sensitive"

    def prepare_arguments(
        self,
        user_input,
        file_path_extractor,
    ):
        return {
            "path": file_path_extractor.extract(
                user_input
            ),
        }

    def run(self, path):
        project_root = Path.home() / "Rebecca"
        target = Path(path).expanduser()

        try:
            target = target.resolve()
            project_root = project_root.resolve()

            if not target.is_relative_to(
                project_root
            ):
                return {
                    "error": (
                        "Por seguridad, solo puedo eliminar "
                        "archivos dentro de ~/Rebecca."
                    )
                }

            if not target.exists():
                return {
                    "error": (
                        f"El archivo no existe: {target}"
                    ),
                    "exists": False,
                }

            if not target.is_file():
                return {
                    "error": (
                        f"La ruta no corresponde a un archivo: "
                        f"{target}"
                    )
                }

            target.unlink()

            return {
                "path": str(target),
                "deleted": True,
            }

        except (OSError, ValueError) as error:
            return {
                "error": str(error)
            }

    def describe_action(
        self,
        kwargs,
    ):
        path = kwargs.get(
            "path",
            "ruta desconocida",
        )

        return (
            "Voy a eliminar el archivo:\n"
            f"{path}\n\n"
            "Esta operación no se puede deshacer "
            "automáticamente."
        )

    def format_result(
        self,
        result,
        user_input="",
    ):
        if not isinstance(result, dict):
            return None

        if result.get("deleted"):
            path = result.get(
                "path",
                "el archivo",
            )

            return (
                f"Archivo eliminado correctamente:\n"
                f"{path}"
            )

        if result.get("error"):
            return (
                f"No pude eliminar el archivo: "
                f"{result['error']}"
            )

        return None

