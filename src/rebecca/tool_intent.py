import re
import unicodedata


class ToolIntentDetector:
    TOOL_PATTERNS = {
        "file_delete": (
            "elimina el archivo",
            "eliminar el archivo",
            "borra el archivo",
            "borrar el archivo",
            "elimina este archivo",
            "eliminar este archivo",
            "borra este archivo",
            "borrar este archivo",
        ),

        "file_modify": (
            "sobrescribe el archivo",
            "sobrescribir el archivo",
            "modifica el archivo",
            "modificar el archivo",
            "cambia el contenido del archivo",
            "cambiar el contenido del archivo",
            "reemplaza el contenido del archivo",
            "reemplazar el contenido del archivo",
            "edita el archivo",
            "editar el archivo",
        ),

        "file_write": (
            "crea un archivo",
            "crear un archivo",
            "escribe un archivo",
            "escribir un archivo",
            "guarda en un archivo",
            "guardar en un archivo",
        ),

        "file_read": (
            "lee el archivo",
            "leer el archivo",
            "abre el archivo",
            "abrir el archivo",
            "muestra el archivo",
            "mostrar el archivo",
            "contenido del archivo",
        ),

        "file_info": (
            "informacion del archivo",
            "información del archivo",
            "datos del archivo",
            "tamaño del archivo",
            "tamano del archivo",
            "que contiene el archivo",
            "qué contiene el archivo",
        ),

        "gmail_read": (
            "lee el correo",
            "leer el correo",
            "abre el correo",
            "abrir el correo",
            "muestra el correo",
            "mostrar el correo",
            "lee este correo",
            "leer este correo",
            "abre este correo",
            "abrir este correo",
        ),

        "gmail_search": (
            "busca en gmail",
            "buscar en gmail",
            "busca correos",
            "buscar correos",
            "busca correo",
            "buscar correo",
            "buscame un correo",
            "buscame correos",
            "busca un correo",
            "buscar un correo",
            "busca emails",
            "buscar emails",
            "busca email",
            "buscar email",
            "busca mensajes",
            "buscar mensajes",
            "busca mis correos",
            "buscar mis correos",
            "busca mis emails",
            "buscar mis emails",
            "busca mis mensajes",
            "buscar mis mensajes",
            "buscame mis correos",
            "buscame mis emails",
            "buscame mis mensajes",
        ),

        "web_open": (
            "abre la pagina",
            "abrir la pagina",
            "abre la página",
            "abrir la página",
            "abre el sitio",
            "abrir el sitio",
            "abre esta pagina",
            "abrir esta pagina",
            "abre esta página",
            "abrir esta página",
            "abre este sitio",
            "abrir este sitio",
            "abre la url",
            "abrir la url",
            "abre este enlace",
            "abrir este enlace",
            "abre el resultado",
            "abrir el resultado",
            "abre el resultado numero",
            "abrir el resultado numero",
            "abre el resultado número",
            "abrir el resultado número",
        ),

        "web_search": (
            "busca en internet",
            "buscar en internet",
            "busca en la internet",
            "buscar en la internet",
            "busca en la web",
            "buscar en la web",
            "busca por internet",
            "buscar por internet",
            "busca en google",
            "buscar en google",
            "busca en bing",
            "buscar en bing",
            "busca en duckduckgo",
            "buscar en duckduckgo",
            "investiga en internet",
            "investigar en internet",
            "investiga en la web",
            "investigar en la web",
            "haz una búsqueda en internet",
            "haz una busqueda en internet",
            "haz una búsqueda en la web",
            "haz una busqueda en la web",
        ),

        "memory_info": (
            "memoria ram",
            "memoria de ram",
            "ram",
            "memoria del sistema",
            "memoria disponible",
            "memoria utilizada",
            "uso de memoria",
            "uso de ram",
            "cuanta ram tengo",
            "cuánta ram tengo",
            "cuanta memoria ram tengo",
            "cuánta memoria ram tengo",
            "cuanta memoria tiene mi pc",
            "cuánta memoria tiene mi pc",
            "cuanta memoria tiene mi computadora",
            "cuánta memoria tiene mi computadora",
            "cuanta memoria estoy usando",
            "cuánta memoria estoy usando",
            "cuanta ram estoy usando",
            "cuánta ram estoy usando",
            "cuanta memoria esta usando mi pc",
            "cuánta memoria está usando mi pc",
            "cuanta memoria usa mi pc",
            "cuánta memoria usa mi pc",
            "cuanta memoria esta usando mi computadora",
            "cuánta memoria está usando mi computadora",
            "cuanta memoria usa mi computadora",
            "cuánta memoria usa mi computadora",
        ),

        "disk_info": (
            "espacio libre",
            "espacio del disco",
            "espacio en disco",
            "disco duro",
            "disco",
            "almacenamiento",
            "cuanto espacio tengo",
            "cuánto espacio tengo",
            "cuanto espacio queda",
            "cuánto espacio queda",
        ),

        "cpu_info": (
            "procesador",
            "cpu",
            "procesador tengo",
            "que procesador tengo",
            "qué procesador tengo",
            "informacion del procesador",
            "información del procesador",
            "informacion de la cpu",
            "información de la cpu",
        ),

        "process_info": (
            "procesos",
            "programas corriendo",
            "programas abiertos",
            "que programas estan corriendo",
            "qué programas están corriendo",
            "que programas tengo abiertos",
            "qué programas tengo abiertos",
            "que se esta ejecutando",
            "qué se está ejecutando",
            "procesos corriendo",
            "procesos activos",
        ),

        "system_info": (
            "informacion del sistema",
            "información del sistema",
            "datos del sistema",
            "sistema operativo",
            "que sistema tengo",
            "qué sistema tengo",
            "version de linux",
            "versión de linux",
            "informacion de mi pc",
            "información de mi pc",
        ),
    }

    PRIORITY = (
        "file_delete",
        "file_modify",
        "file_write",
        "file_read",
        "file_info",
        "gmail_read",
        "gmail_search",
        "web_open",
        "web_search",
        "memory_info",
        "disk_info",
        "cpu_info",
        "process_info",
        "system_info",
    )

    def detect(self, user_input):
        detected_tools = self.detect_all(
            user_input
        )

        if not detected_tools:
            return None

        return detected_tools[0]

    def detect_all(self, user_input):
        normalized = self._normalize(
            user_input
        )

        detected_tools = []

        for tool_name in self.PRIORITY:
            patterns = self.TOOL_PATTERNS.get(
                tool_name,
                (),
            )

            for pattern in patterns:
                normalized_pattern = (
                    self._normalize(pattern)
                )

                if self._contains_phrase(
                    normalized,
                    normalized_pattern,
                ):
                    detected_tools.append(
                        tool_name
                    )
                    break

        return detected_tools

    def _normalize(self, text):
        text = text.lower().strip()

        text = unicodedata.normalize(
            "NFD",
            text,
        )

        text = "".join(
            char
            for char in text
            if unicodedata.category(char)
            != "Mn"
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text

    def _contains_phrase(
        self,
        text,
        phrase,
    ):
        pattern = (
            r"(?<!\w)"
            + re.escape(phrase)
            + r"(?!\w)"
        )

        return re.search(
            pattern,
            text,
        ) is not None

