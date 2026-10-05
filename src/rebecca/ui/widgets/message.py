from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)


class MessageWidget(QFrame):
    def __init__(
        self,
        sender,
        message,
        parent=None,
    ):
        super().__init__(parent)

        self.sender = sender
        self.message = message

        self._build_ui()

    def _build_ui(self):
        is_user = self.sender == "Tú"

        container = QHBoxLayout(self)

        container.setContentsMargins(
            8,
            5,
            8,
            5,
        )

        container.setSpacing(0)

        bubble = QFrame()

        bubble.setMaximumWidth(650)

        bubble_layout = QVBoxLayout(
            bubble
        )

        bubble_layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )

        bubble_layout.setSpacing(6)

        sender_label = QLabel(
            self.sender
        )

        sender_font = QFont()
        sender_font.setPointSize(10)
        sender_font.setBold(True)

        sender_label.setFont(
            sender_font
        )

        message_label = QLabel(
            self.message
        )

        message_label.setWordWrap(
            True
        )

        message_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        message_label.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Minimum,
        )

        message_font = QFont()
        message_font.setPointSize(11)

        message_label.setFont(
            message_font
        )

        bubble_layout.addWidget(
            sender_label
        )

        bubble_layout.addWidget(
            message_label
        )

        if is_user:
            bubble.setStyleSheet(
                """
                QFrame {
                    background-color: #294875;
                    border-radius: 15px;
                }
                """
            )

            sender_label.setStyleSheet(
                """
                color: #a9caff;
                """
            )

            message_label.setStyleSheet(
                """
                color: #f5f8ff;
                """
            )

            container.addStretch()

            container.addWidget(
                bubble
            )

        else:
            bubble.setStyleSheet(
                """
                QFrame {
                    background-color: #1a1c20;
                    border: 1px solid #30343a;
                    border-radius: 15px;
                }
                """
            )

            sender_label.setStyleSheet(
                """
                color: #78e0a0;
                """
            )

            message_label.setStyleSheet(
                """
                color: #eeeeee;
                """
            )

            container.addWidget(
                bubble
            )

            container.addStretch()

