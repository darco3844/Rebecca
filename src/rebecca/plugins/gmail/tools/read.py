import base64

from src.rebecca.tools.tool import Tool


class GmailReadTool(Tool):
    name = "gmail_read"

    description = (
        "Lee el contenido y los metadatos "
        "de un correo específico de Gmail."
    )

    permission = "read"

    def __init__(self):
        self.gmail_service = None

    def prepare_arguments(
        self,
        user_input,
        file_path_extractor=None,
    ):
        text = user_input.strip()
        parts = text.split()

        message_id = None

        for part in parts:
            if part.startswith("gmail:"):
                message_id = part[len("gmail:"):]
                break

            if part.startswith("id:"):
                message_id = part[len("id:"):]
                break

        return {
            "message_id": message_id,
        }

    def run(self, message_id=None):
        if self.gmail_service is None:
            raise RuntimeError(
                "GmailReadTool no tiene servicio de Gmail."
            )

        if not message_id:
            raise ValueError(
                "gmail_read necesita un ID de mensaje."
            )

        response = (
            self.gmail_service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full",
            )
            .execute()
        )

        return self._parse_message(response)

    def format_result(
        self,
        result,
        user_input="",
    ):
        if not isinstance(result, dict):
            return None

        subject = (
            result.get("subject")
            or "(Sin asunto)"
        )

        sender = (
            result.get("from")
            or "Remitente desconocido"
        )

        recipient = (
            result.get("to")
            or "Destinatario desconocido"
        )

        date = (
            result.get("date")
            or "Fecha desconocida"
        )

        body = (
            result.get("body")
            or ""
        ).strip()

        snippet = (
            result.get("snippet")
            or ""
        ).strip()

        lines = [
            "Correo de Gmail:",
            "",
            f"Asunto: {subject}",
            f"De: {sender}",
            f"Para: {recipient}",
            f"Fecha: {date}",
        ]

        cc = result.get("cc")

        if cc:
            lines.append(
                f"CC: {cc}"
            )

        lines.extend([
            "",
            "Contenido:",
        ])

        if body:
            lines.append(body)
        elif snippet:
            lines.append(snippet)
        else:
            lines.append(
                "(El correo no contiene "
                "texto disponible.)"
            )

        return "\n".join(lines)

    def _parse_message(self, message):
        headers = self._get_headers(message)

        payload = message.get(
            "payload",
            {},
        )

        body = self._extract_body(
            payload
        )

        return {
            "id": message.get("id"),
            "thread_id": message.get("threadId"),
            "from": headers.get("From"),
            "to": headers.get("To"),
            "cc": headers.get("Cc"),
            "subject": headers.get("Subject"),
            "date": headers.get("Date"),
            "snippet": message.get(
                "snippet",
                "",
            ),
            "body": body,
            "labels": message.get(
                "labelIds",
                [],
            ),
        }

    def _get_headers(self, message):
        headers = {}

        payload = message.get(
            "payload",
            {},
        )

        for header in payload.get(
            "headers",
            [],
        ):
            name = header.get("name")
            value = header.get(
                "value",
                "",
            )

            if name:
                headers[name] = value

        return headers

    def _extract_body(self, part):
        mime_type = part.get(
            "mimeType",
            "",
        )

        body_data = (
            part.get("body", {})
            .get("data")
        )

        if body_data and (
            mime_type.startswith(
                "text/plain"
            )
            or mime_type.startswith(
                "text/html"
            )
        ):
            return self._decode_body(
                body_data
            )

        for child in part.get(
            "parts",
            [],
        ):
            result = self._extract_body(
                child
            )

            if result:
                return result

        return ""

    def _decode_body(self, data):
        try:
            decoded = (
                base64.urlsafe_b64decode(
                    data
                    + "="
                    * (-len(data) % 4)
                )
            )

            return decoded.decode(
                "utf-8",
                errors="replace",
            )

        except Exception:
            return ""

