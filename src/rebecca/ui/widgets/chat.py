from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.rebecca.ui.widgets.message import (
    MessageWidget,
)


class ChatWidget(QFrame):
    message_sent = None

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet(
            """
            QFrame {
                background-color: #101114;
            }
            """
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            10
        )

        self.chat_scroll = QScrollArea()

        self.chat_scroll.setWidgetResizable(
            True
        )

        self.chat_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.chat_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.chat_scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.chat_scroll.setStyleSheet(
            """
            QScrollArea {
                background-color: #101114;
                border: none;
            }

            QScrollBar:vertical {
                background: #101114;
                width: 10px;
                margin: 3px;
            }

            QScrollBar::handle:vertical {
                background: #34383f;
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #4a4f57;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            """
        )

        self.chat_container = QWidget()

        self.chat_container.setStyleSheet(
            """
            QWidget {
                background-color: #101114;
            }
            """
        )

        self.chat_layout = QVBoxLayout(
            self.chat_container
        )

        self.chat_layout.setContentsMargins(
            18,
            18,
            18,
            18,
        )

        self.chat_layout.setSpacing(
            7
        )

        self.chat_layout.addStretch()

        self.chat_scroll.setWidget(
            self.chat_container
        )

        layout.addWidget(
            self.chat_scroll,
            1,
        )

        input_frame = QFrame()

        input_frame.setStyleSheet(
            """
            QFrame {
                background-color: #17191d;
                border: 1px solid #2d3036;
                border-radius: 14px;
            }
            """
        )

        input_layout = QHBoxLayout(
            input_frame
        )

        input_layout.setContentsMargins(
            10,
            7,
            7,
            7,
        )

        input_layout.setSpacing(
            8
        )

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Escribe un mensaje..."
        )

        self.input.setMinimumHeight(
            42
        )

        self.input.setStyleSheet(
            """
            QLineEdit {
                border: none;
                background: transparent;
                color: #eeeeee;
                font-size: 14px;
                padding: 6px;
            }

            QLineEdit:focus {
                border: none;
            }
            """
        )

        input_layout.addWidget(
            self.input,
            1,
        )

        self.send_button = QPushButton(
            "Enviar"
        )

        self.send_button.setMinimumHeight(
            40
        )

        self.send_button.setMinimumWidth(
            90
        )

        self.send_button.setCursor(
            Qt.PointingHandCursor
        )

        self.send_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                border-radius: 10px;
                background-color: #315f9f;
                color: white;
                font-size: 13px;
                font-weight: bold;
                padding: 0 16px;
            }

            QPushButton:hover {
                background-color: #3c70b8;
            }

            QPushButton:pressed {
                background-color: #284e84;
            }

            QPushButton:disabled {
                background-color: #292c31;
                color: #686b70;
            }
            """
        )

        input_layout.addWidget(
            self.send_button
        )

        layout.addWidget(
            input_frame
        )

    def add_message(
        self,
        sender,
        message,
    ):
        widget = MessageWidget(
            sender,
            message,
        )

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            widget,
        )

        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        scrollbar = (
            self.chat_scroll.verticalScrollBar()
        )

        scrollbar.setValue(
            scrollbar.maximum()
        )

    def set_input_enabled(
        self,
        enabled,
    ):
        self.input.setEnabled(
            enabled
        )

        self.send_button.setEnabled(
            enabled
        )

    def get_input_text(self):
        return (
            self.input.text()
            .strip()
        )

    def clear_input(self):
        self.input.clear()

