from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class SidebarButton(QPushButton):
    def __init__(
        self,
        text,
        parent=None,
    ):
        super().__init__(
            text,
            parent,
        )

        self.setMinimumHeight(
            42
        )

        self.setCursor(
            Qt.PointingHandCursor
        )

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        self.setStyleSheet(
            """
            QPushButton {
                text-align: left;
                border: none;
                border-radius: 9px;
                background-color: transparent;
                color: #b7bbc2;
                font-size: 13px;
                padding: 0 14px;
            }

            QPushButton:hover {
                background-color: #202329;
                color: #eeeeee;
            }

            QPushButton:pressed {
                background-color: #282c33;
            }
            """
        )


class SidebarWidget(QFrame):
    navigation_requested = Signal(str)

    def __init__(
        self,
        parent=None,
    ):
        super().__init__(parent)

        self._build_ui()

    def _build_ui(self):
        self.setFixedWidth(
            220
        )

        self.setStyleSheet(
            """
            QFrame {
                background-color: #15171a;
                border-right: 1px solid #292c31;
            }
            """
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            14,
            18,
            14,
            18,
        )

        layout.setSpacing(
            7
        )

        logo = QLabel(
            "REBECCA"
        )

        logo_font = QFont()
        logo_font.setPointSize(18)
        logo_font.setBold(True)

        logo.setFont(
            logo_font
        )

        logo.setStyleSheet(
            """
            color: #f0f0f0;
            padding-left: 8px;
            """
        )

        layout.addWidget(
            logo
        )

        subtitle = QLabel(
            "Asistente personal"
        )

        subtitle.setStyleSheet(
            """
            color: #6f747c;
            font-size: 11px;
            padding-left: 9px;
            """
        )

        layout.addWidget(
            subtitle
        )

        status = QLabel(
            "●  En línea"
        )

        status.setStyleSheet(
            """
            color: #6ee7a8;
            font-size: 11px;
            padding: 8px 9px;
            """
        )

        layout.addWidget(
            status
        )

        separator = QFrame()

        separator.setFrameShape(
            QFrame.HLine
        )

        separator.setStyleSheet(
            """
            color: #292c31;
            """
        )

        layout.addWidget(
            separator
        )

        new_chat = SidebarButton(
            "＋  Nueva conversación"
        )

        new_chat.clicked.connect(
            lambda: self.navigation_requested.emit(
                "new_chat"
            )
        )

        layout.addWidget(
            new_chat
        )

        memory = SidebarButton(
            "🧠  Memoria"
        )

        memory.clicked.connect(
            lambda: self.navigation_requested.emit(
                "memory"
            )
        )

        layout.addWidget(
            memory
        )

        tools = SidebarButton(
            "🔧  Herramientas"
        )

        tools.clicked.connect(
            lambda: self.navigation_requested.emit(
                "tools"
            )
        )

        layout.addWidget(
            tools
        )

        plugins = SidebarButton(
            "🧩  Plugins"
        )

        plugins.clicked.connect(
            lambda: self.navigation_requested.emit(
                "plugins"
            )
        )

        layout.addWidget(
            plugins
        )

        system = SidebarButton(
            "💻  Sistema"
        )

        system.clicked.connect(
            lambda: self.navigation_requested.emit(
                "system"
            )
        )

        layout.addWidget(
            system
        )

        layout.addStretch()

        settings = SidebarButton(
            "⚙  Configuración"
        )

        settings.clicked.connect(
            lambda: self.navigation_requested.emit(
                "settings"
            )
        )

        layout.addWidget(
            settings
        )

