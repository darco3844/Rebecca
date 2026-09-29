class IntentDetector:
    def detect(self, text):
        text = text.lower().strip()

        # Guardar memoria
        if (
            text.startswith("recuerda ")
            or text.startswith("acuérdate de ")
            or text.startswith("acuerdate de ")
            or text.startswith("guarda ")
        ):
            return "remember"

        # Consultar memoria
        if (
            "qué recuerdas" in text
            or "que recuerdas" in text
            or "qué recuerdo" in text
            or "que recuerdo" in text
            or text.startswith("recuerdas ")
        ):
            return "recall_memory"

        # Olvidar memoria
        if (
            text.startswith("olvida ")
            or text.startswith("olvidar ")
            or "olvida el recuerdo" in text
        ):
            return "forget_memory"

        # Identidad
        if (
            "cómo te llamas" in text
            or "como te llamas" in text
            or "quién eres" in text
            or "quien eres" in text
            or "cómo te defines" in text
            or "como te defines" in text
            or "qué personalidad tienes" in text
            or "que personalidad tienes" in text
        ):
            return "identity"

        # Proyecto
        if (
            "qué estamos construyendo" in text
            or "que estamos construyendo" in text
            or "qué es rebecca" in text
            or "que es rebecca" in text
            or "qué tenemos funcionando" in text
            or "que tenemos funcionando" in text
        ):
            return "project_knowledge"

        return "conversation"
