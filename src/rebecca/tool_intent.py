import re
import unicodedata


class ToolIntentDetector:
    INTENTS = {
        "system_info": [
            "sistema operativo",
            "sistema",
            "linux",
            "cachyos",
            "distribucion",
            "kernel",
            "hostname",
            "arquitectura",
        ],
        "memory_info": [
            "ram",
            "memoria ram",
            "memoria disponible",
            "memoria libre",
            "memoria usada",
            "memoria utilizada",
        ],
        "disk_info": [
            "disco",
            "discos",
            "almacenamiento",
            "espacio libre",
            "espacio disponible",
            "espacio usado",
            "espacio utilizado",
        ],
        "cpu_info": [
            "cpu",
            "procesador",
            "procesadores",
            "nucleos",
            "hilos",
            "chip",
        ],
        "process_info": [
            "procesos",
            "proceso",
            "programas ejecutandose",
            "programas activos",
            "programas corriendo",
            "programas que estan corriendo",
            "programas que estan activos",
            "que programas estan corriendo",
            "que programas estan activos",
            "que esta ejecutandose",
            "que esta corriendo",
            "que procesos estan corriendo",
            "que procesos estan activos",
            "procesos activos",
            "procesos corriendo",
            "procesos ejecutandose",
        ],
        "file_write": [
            "crea un archivo",
            "crear un archivo",
            "crea archivo",
            "crear archivo",
            "escribe en el archivo",
            "escribir en el archivo",
            "escribe el archivo",
            "escribir el archivo",
            "guarda en el archivo",
            "guardar en el archivo",
            "guarda esto en",
            "guardar esto en",
            "crea un texto",
            "crear un texto",
        ],
        "file_read": [
            "lee el archivo",
            "leer el archivo",
            "lee archivo",
            "leer archivo",
            "muestrame el archivo",
            "mostrar el archivo",
            "contenido del archivo",
            "que dice el archivo",
            "abre el archivo",
        ],
        "file_info": [
            "archivos",
            "archivo",
            "carpeta",
            "carpetas",
            "directorio",
            "directorios",
            "que hay en",
            "que contiene",
            "lista los archivos",
            "listar archivos",
        ],
    }

    PRIORITY = [
        "file_write",
        "file_read",
        "file_info",
        "memory_info",
        "disk_info",
        "cpu_info",
        "process_info",
        "system_info",
    ]

    def detect(self, text):
        normalized = self._normalize(text)

        if not normalized:
            return None

        for intent in self.PRIORITY:
            phrases = self.INTENTS[intent]

            if self._matches(
                normalized,
                phrases,
            ):
                return intent

        return None

    def _matches(
        self,
        text,
        phrases,
    ):
        for phrase in phrases:
            if self._phrase_matches(
                text,
                phrase,
            ):
                return True

        return False

    def _phrase_matches(
        self,
        text,
        phrase,
    ):
        phrase = self._normalize(
            phrase
        )

        if not phrase:
            return False

        pattern = (
            r"(?<!\w)"
            + re.escape(phrase)
            + r"(?!\w)"
        )

        return re.search(
            pattern,
            text,
        ) is not None

    def _normalize(self, text):
        text = str(text).lower().strip()

        text = unicodedata.normalize(
            "NFD",
            text,
        )

        text = "".join(
            character
            for character in text
            if unicodedata.category(character)
            != "Mn"
        )

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text
