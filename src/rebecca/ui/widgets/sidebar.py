from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QHBoxLayout, QWidget
from src.rebecca.ui.widgets.avatar import AvatarWidget

class SidebarButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(42)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("QPushButton { text-align: left; border: none; border-radius: 9px; background-color: transparent; color: #b7bbc2; font-size: 13px; padding: 0 14px; } QPushButton:hover { background-color: #202329; color: #eeeeee; } QPushButton:pressed { background-color: #282c33; }")

class SidebarWidget(QFrame):
    navigation_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        self.setFixedWidth(220)
        self.setStyleSheet("QFrame { background-color: #15171a; border-right: 1px solid #292c31; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 18)
        layout.setSpacing(7)

        title = QLabel("REBECCA")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #f0f0f0; padding-top: 2px;")
        layout.addWidget(title)

        subtitle = QLabel("ASISTENTE PERSONAL")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #6f747c; font-size: 9px; letter-spacing: 1px;")
        layout.addWidget(subtitle)

        self.avatar = AvatarWidget()
        self.avatar.setFixedSize(180, 180)

        avatar_container = QWidget()
        avatar_layout = QHBoxLayout(avatar_container)
        avatar_layout.setContentsMargins(0, 10, 0, 8)
        avatar_layout.setAlignment(Qt.AlignCenter)
        avatar_layout.addWidget(self.avatar)
        layout.addWidget(avatar_container)

        self.status = QLabel("●  EN LÍNEA")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color: #6ee7a8; font-size: 10px; font-weight: bold; letter-spacing: 1px; padding-bottom: 8px;")
        layout.addWidget(self.status)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #292c31;")
        layout.addWidget(separator)

        buttons = [
            ("＋  Nueva conversación", "new_chat"),
            ("🧠  Memoria", "memory"),
            ("🔧  Herramientas", "tools"),
            ("🧩  Plugins", "plugins"),
            ("💻  Sistema", "system"),
            ("⚙  Configuración", "settings"),
        ]

        for text, target in buttons:
            button = SidebarButton(text)
            button.clicked.connect(lambda checked=False, value=target: self.navigation_requested.emit(value))
            layout.addWidget(button)

        layout.addStretch()
