from pathlib import Path

from src.rebecca.tools.tool import Tool


class FileModifyTool(Tool):
    name = "file_modify"

    description = (
        "Modifica el contenido de un archivo de texto "
        "existente dentro del proyecto Rebecca."
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
            "content": self._extract_modify_content(
                user_input
            ),
        }

    def run(self, path, content):
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
                        "Por seguridad, solo puedo modificar "
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

            target.write_text(
                content,
                encoding="utf-8",
            )

            return {
                "path": str(target),
                "modified": True,
                "characters": len(content),
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

        content = kwargs.get(
            "content",
            "",
        )

        return (
            "Voy a modificar el archivo:\n"
            f"{path}\n\n"
            "Nuevo contenido:\n"
            f"{content}"
        )

    def _extract_modify_content(
        self,
        text,
    ):
        markers = [
            "que diga ",
            "que dice ",
            "con el contenido ",
            "con el texto ",
            "contenido ",
            "texto ",
        ]

        lower_text = text.lower()

        for marker in markers:
            position = lower_text.find(
                marker
            )

            if position != -1:
                return text[
                    position + len(marker):
                ].strip()

        return ""

