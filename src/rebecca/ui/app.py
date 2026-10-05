import sys

from PySide6.QtWidgets import QApplication

from src.rebecca.brain import Brain
from src.rebecca.cognitive import CognitiveEngine
from src.rebecca.ui.window import ChatWindow


def main():
    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "Rebecca"
    )

    brain = Brain()

    engine = CognitiveEngine(
        brain=brain
    )

    window = ChatWindow(
        engine
    )

    window.show()

    return app.exec()

