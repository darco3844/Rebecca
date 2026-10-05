from src.rebecca.tools.tool import Tool


class GmailSearchTool(Tool):
    name = "gmail_search"

    description = (
        "Busca correos electrónicos en Gmail "
        "usando lenguaje natural o sintaxis "
        "de búsqueda de Gmail."
    )

    permission = "read"

    SEARCH_PREFIXES = (
        "busca en gmail ",
        "buscar en gmail ",
        "busca mis correos ",
        "buscar mis correos ",
        "buscame mis correos ",
        "búscame mis correos ",
        "busca mis emails ",
        "buscar mis emails ",
        "buscame mis emails ",
        "búscame mis emails ",
        "busca mis mensajes ",
        "buscar mis mensajes ",
        "buscame mis mensajes ",
        "búscame mis mensajes ",
        "busca correos ",
        "buscar correos ",
        "buscame correos ",
        "búscame correos ",
        "busca correo ",
        "buscar correo ",
        "buscame un correo ",
        "búscame un correo ",
        "busca un correo ",
        "buscar un correo ",
        "busca emails ",
        "buscar emails ",
        "busca email ",
        "buscar email ",
        "busca mensajes ",
        "buscar mensajes ",
    )

    NATURAL_SUBJECT_PREFIXES = (
        "sobre ",
        "acerca de ",
        "relacionados con ",
        "relacionado con ",
    )

    NATURAL_SENDER_PREFIXES = (
        "de ",
        "del ",
        "desde ",
        "enviados por ",
        "enviado por ",
        "que me envio ",
        "que me envió ",
    )

    SNIPPET_MAX_LENGTH = 100

    def __init__(self):
        self.gmail_service = None

    def prepare_arguments(
        self,
        user_input,
        file_path_extractor=None,
    ):
        query = self._extract_query(user_input)

        return {
            "query": query,
            "max_results": 5,
        }

    def run(
        self,
        query="",
        max_results=5,
    ):
        if self.gmail_service is None:
            raise RuntimeError(
                "GmailSearchTool no tiene servicio de Gmail."
            )

        response = (
            self.gmail_service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=max_results,
            )
            .execute()
        )

        messages = response.get(
            "messages",
            [],
        )

        detailed_messages = []

        for message in messages:
            message_id = message.get("id")

            if not message_id:
                continue

            try:
                detailed = (
                    self.gmail_service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=message_id,
                        format="metadata",
                        metadataHeaders=[
                            "From",
                            "Subject",
                            "Date",
                        ],
                    )
                    .execute()
                )

                detailed_messages.append(
                    self._parse_message_metadata(
                        detailed
                    )
                )

            except Exception as error:
                detailed_messages.append(
                    {
                        "id": message_id,
                        "error": str(error),
                    }
                )

        return {
            "query": query,
            "count": len(detailed_messages),
            "messages": detailed_messages,
        }

    def format_result(
        self,
        result,
        user_input="",
    ):
        if not isinstance(
            result,
            dict,
        ):
            return None

        messages = result.get(
            "messages",
            [],
        )

        if not messages:
            return (
                "No encontré correos que coincidan "
                "con la búsqueda."
            )

        lines = [
            "He encontrado estos correos de Gmail:"
        ]

        for index, message in enumerate(
            messages,
            start=1,
        ):
            if message.get("error"):
                continue

            subject = (
                message.get("subject")
                or "(Sin asunto)"
            )

            date = (
                message.get("date")
                or "Fecha desconocida"
            )

            sender = (
                message.get("from")
                or "Remitente desconocido"
            )

            snippet = (
                message.get("snippet")
                or ""
            )

            lines.append("")
            lines.append(
                f"{index}. {subject}"
            )
            lines.append(
                f"   De: {sender}"
            )
            lines.append(
                f"   Fecha: {date}"
            )

            if snippet:
                lines.append(
                    f"   Resumen: {snippet}"
                )

        return "\n".join(lines)

    def _parse_message_metadata(
        self,
        message,
    ):
        headers = self._get_headers(
            message
        )

        snippet = message.get(
            "snippet",
            "",
        )

        snippet = self._truncate_snippet(
            snippet
        )

        return {
            "id": message.get("id"),
            "from": headers.get("From"),
            "subject": headers.get("Subject"),
            "date": headers.get("Date"),
            "snippet": snippet,
        }

    def _truncate_snippet(
        self,
        snippet,
    ):
        if not snippet:
            return ""

        snippet = snippet.strip()

        if len(snippet) <= self.SNIPPET_MAX_LENGTH:
            return snippet

        return (
            snippet[
                : self.SNIPPET_MAX_LENGTH
            ].rstrip()
            + "..."
        )

    def _get_headers(
        self,
        message,
    ):
        headers = {}

        payload = message.get(
            "payload",
            {},
        )

        for header in payload.get(
            "headers",
            [],
        ):
            name = header.get(
                "name"
            )

            value = header.get(
                "value",
                "",
            )

            if name:
                headers[name] = value

        return headers

    def _extract_query(
        self,
        user_input,
    ):
        text = user_input.strip()
        normalized = text.lower()

        for prefix in self.SEARCH_PREFIXES:
            if normalized.startswith(
                prefix
            ):
                query = text[
                    len(prefix):
                ].strip()

                return self._clean_natural_query(
                    query
                )

        return text

    def _clean_natural_query(
        self,
        query,
    ):
        cleaned = query.strip()
        normalized = cleaned.lower()

        for prefix in self.NATURAL_SUBJECT_PREFIXES:
            if normalized.startswith(
                prefix
            ):
                subject = cleaned[
                    len(prefix):
                ].strip()

                if subject:
                    return subject

        for prefix in self.NATURAL_SENDER_PREFIXES:
            if normalized.startswith(
                prefix
            ):
                sender = cleaned[
                    len(prefix):
                ].strip()

                if sender:
                    return (
                        f'from:("{sender}")'
                    )

        return cleaned

