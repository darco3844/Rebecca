class ToolIntentDetector:
    def detect(self, text):
        text = text.lower().strip()

        # ==========================================
        # INFORMACIÓN DEL SISTEMA
        # ==========================================

        if self._matches(
            text,
            [
                "sistema",
                "linux",
                "cachyos",
                "distribución",
                "distribucion",
                "kernel",
                "hostname",
                "arquitectura",
            ],
        ):
            return "system_info"

        # ==========================================
        # MEMORIA RAM
        # ==========================================

        if self._matches(
            text,
            [
                "ram",
                "memoria ram",
                "memoria disponible",
                "memoria libre",
                "cuánta memoria",
                "cuanta memoria",
            ],
        ):
            return "memory_info"

        # ==========================================
        # DISCO
        # ==========================================

        if self._matches(
            text,
            [
                "disco",
                "discos",
                "almacenamiento",
                "espacio libre",
                "espacio disponible",
                "cuánto espacio",
                "cuanto espacio",
            ],
        ):
            return "disk_info"

        # ==========================================
        # CPU
        # ==========================================

        if self._matches(
            text,
            [
                "cpu",
                "procesador",
                "procesadores",
                "núcleos",
                "nucleos",
                "hilos",
            ],
        ):
            return "cpu_info"

        # ==========================================
        # PROCESOS
        # ==========================================

        if self._matches(
            text,
            [
                "procesos",
                "proceso",
                "programas ejecutándose",
                "programas ejecutandose",
                "qué está ejecutándose",
                "que esta ejecutandose",
            ],
        ):
            return "process_info"

        # ==========================================
        # ESCRIBIR / CREAR ARCHIVOS
        # ==========================================

        if self._matches(
            text,
            [
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
        ):
            return "file_write"

        # ==========================================
        # LEER ARCHIVOS
        # ==========================================

        if self._matches(
            text,
            [
                "lee el archivo",
                "leer el archivo",
                "lee archivo",
                "leer archivo",
                "muéstrame el archivo",
                "muestrame el archivo",
                "contenido del archivo",
                "qué dice el archivo",
                "que dice el archivo",
                "abre el archivo",
            ],
        ):
            return "file_read"

        # ==========================================
        # INFORMACIÓN DE ARCHIVOS
        # ==========================================

        if self._matches(
            text,
            [
                "archivos",
                "archivo",
                "carpeta",
                "carpetas",
                "directorio",
                "directorios",
                "qué hay en",
                "que hay en",
                "qué contiene",
                "que contiene",
                "lista los archivos",
                "listar archivos",
            ],
        ):
            return "file_info"

        return None

    def _matches(self, text, phrases):
        return any(
            phrase in text
            for phrase in phrases
        )
