from pathlib import Path

from src.rebecca.tools.tool import Tool


class FileWriteTool(Tool):
    name = "file_write"

    description = (
        "Crea un archivo de texto nuevo dentro "
        "del proyecto Rebecca."
    )

    def prepare_arguments(
        self,
        user_input,
        file_path_extractor,
    ):
        return {
            "path": file_path_extractor.extract(
                user_input
            ),
            "content": self._extract_write_content(
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
                        "Por seguridad, solo puedo crear "
                        "archivos dentro de ~/Rebecca."
                    )
                }

            if target.exists():
                return {
                    "error": (
                        f"El archivo ya existe: {target}"
                    ),
                    "exists": True,
                }

            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            target.write_text(
                content,
                encoding="utf-8",
            )

            return {
                "path": str(target),
                "created": True,
                "characters": len(content),
            }

        except (OSError, ValueError) as error:
            return {
                "error": str(error)
            }

    def _extract_write_content(self, text):
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
            position = lower_text.find(marker)

            if position != -1:
                return text[
                    position + len(marker):
                ].strip()

        return ""
