from pathlib import Path

from src.rebecca.tools.tool import Tool


class FileReadTool(Tool):
    name = "file_read"

    description = (
        "Lee el contenido de un archivo de texto."
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

    def run(
        self,
        path,
        max_chars=12000,
    ):
        target = Path(path).expanduser()

        try:
            if not target.exists():
                return {
                    "error": f"No existe: {target}"
                }

            if not target.is_file():
                return {
                    "error": f"No es un archivo: {target}"
                }

            content = target.read_text(
                encoding="utf-8",
                errors="replace",
            )

            truncated = len(content) > max_chars

            if truncated:
                content = content[:max_chars]

            return {
                "path": str(target.resolve()),
                "content": content,
                "truncated": truncated,
                "characters": len(content),
            }

        except (OSError, UnicodeError) as error:
            return {
                "error": str(error)
            }
