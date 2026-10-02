from src.rebecca.memory_classifier import (
    MemoryClassifier,
)


class MemoryDecision:
    def __init__(self, classifier=None):
        if classifier is None:
            classifier = MemoryClassifier()

        self.classifier = classifier

    def decide(self, content):
        text = content.strip()

        if not text:
            return {
                "should_remember": False,
                "memory_type": "general",
                "importance": 1,
                "memory_level": "temporary",
                "memory_key": None,
            }

        if self._is_question(text):
            return {
                "should_remember": False,
                "memory_type": "general",
                "importance": 1,
                "memory_level": "temporary",
                "memory_key": None,
            }

        memory_type = self.classifier.classify(
            text
        )

        if memory_type == "preference":
            importance = 6
            memory_level = "long_term"

        elif memory_type == "project":
            importance = 8
            memory_level = "long_term"

        elif memory_type == "goal":
            importance = 8
            memory_level = "long_term"

        elif memory_type == "relationship":
            importance = 9
            memory_level = "core"

        elif memory_type == "configuration":
            importance = 6
            memory_level = "working"

        else:
            return {
                "should_remember": False,
                "memory_type": "general",
                "importance": 3,
                "memory_level": "temporary",
                "memory_key": None,
            }

        memory_key = self.classifier.generate_key(
            text,
            memory_type,
        )

        return {
            "should_remember": True,
            "memory_type": memory_type,
            "importance": importance,
            "memory_level": memory_level,
            "memory_key": memory_key,
        }

    def _is_question(self, text):
        stripped = text.strip()

        if "?" in stripped or "¿" in stripped:
            return True

        normalized = (
            stripped.lower()
            .replace("á", "a")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ú", "u")
        )

        question_starters = (
            "que ",
            "que es ",
            "cual ",
            "cuales ",
            "como ",
            "cuando ",
            "donde ",
            "quien ",
            "quienes ",
            "por que ",
            "porque ",
            "cuanto ",
            "cuanta ",
            "cuantos ",
            "cuantas ",
        )

        return normalized.startswith(
            question_starters
        )
