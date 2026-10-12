from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class PluginToolRow(QFrame):
    def __init__(
        self,
        tool,
        parent=None,
    ):
        super().__init__(parent)

        self.setStyleSheet(
            """
            QFrame {
                background-color: #141619;
                border: 1px solid #292d33;
                border-radius: 9px;
            }
            """
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            12,
            9,
            12,
            9,
        )

        layout.setSpacing(
            10
        )

        name = QLabel(
            tool.get(
                "name",
                "Herramienta",
            )
        )

        name.setStyleSheet(
            """
            color: #dedfe2;
            font-size: 12px;
            font-weight: bold;
            """
        )

        description = QLabel(
            tool.get(
                "description",
                "",
            )
        )

        description.setWordWrap(
            True
        )

        description.setStyleSheet(
            """
            color: #777c84;
            font-size: 11px;
            """
        )

        permission = QLabel(
            tool.get(
                "permission",
                "read",
            )
        )

        permission.setAlignment(
            Qt.AlignCenter
        )

        permission.setMinimumWidth(
            65
        )

        permission.setStyleSheet(
            """
            QLabel {
                background-color: #20242a;
                color: #aeb4bd;
                border-radius: 7px;
                padding: 5px 8px;
                font-size: 10px;
                font-weight: bold;
            }
            """
        )

        text_layout = QVBoxLayout()

        text_layout.setSpacing(
            2
        )

        text_layout.addWidget(
            name
        )

        text_layout.addWidget(
            description
        )

        layout.addLayout(
            text_layout,
            1,
        )

        layout.addWidget(
            permission
        )


class PluginCard(QFrame):
    def __init__(
        self,
        plugin,
        config,
        plugin_manager,
        parent=None,
    ):
        super().__init__(parent)

        self.plugin_name = plugin.get(
            "name",
            "Plugin",
        )

        self.config = config
        self.plugin_manager = plugin_manager

        self.setStyleSheet(
            """
            QFrame {
                background-color: #17191d;
                border: 1px solid #292d33;
                border-radius: 14px;
            }
            """
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )

        layout.setSpacing(
            12
        )

        header = QHBoxLayout()

        title_layout = QVBoxLayout()

        title_layout.setSpacing(
            3
        )

        title = QLabel(
            self.plugin_name
        )

        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setBold(True)

        title.setFont(
            title_font
        )

        title.setStyleSheet(
            """
            color: #f0f0f0;
            """
        )

        description = QLabel(
            plugin.get(
                "description",
                "",
            )
        )

        description.setWordWrap(
            True
        )

        description.setStyleSheet(
            """
            color: #777c84;
            font-size: 11px;
            """
        )

        version = QLabel(
            f"Versión {plugin.get('version', '1.0.0')}"
        )

        version.setStyleSheet(
            """
            color: #5f646c;
            font-size: 10px;
            """
        )

        title_layout.addWidget(
            title
        )

        title_layout.addWidget(
            description
        )

        title_layout.addWidget(
            version
        )

        header.addLayout(
            title_layout,
            1,
        )

        enabled = False
        loaded = False

        try:
            enabled = bool(
                self.config.is_enabled(
                    self.plugin_name
                )
            )
        except Exception:
            enabled = False

        try:
            loaded = bool(
                self.plugin_manager.has_plugin(
                    self.plugin_name
                )
            )
        except Exception:
            loaded = False

        if loaded:
            status_text = "● Activo"
            status_color = "#6ee7a8"

        elif enabled:
            status_text = "● No cargado"
            status_color = "#f6c85f"

        else:
            status_text = "● Inactivo"
            status_color = "#747982"

        status = QLabel(
            status_text
        )

        status.setAlignment(
            Qt.AlignCenter
        )

        status.setStyleSheet(
            f"""
            QLabel {{
                color: {status_color};
                background-color: #20242a;
                border-radius: 8px;
                padding: 7px 10px;
                font-size: 10px;
                font-weight: bold;
            }}
            """
        )

        header.addWidget(
            status
        )

        layout.addLayout(
            header
        )

        error_message = plugin.get("error")
        if error_message:
            error_label = QLabel(
                f"No se pudo iniciar este plugin: {error_message}"
            )
            error_label.setWordWrap(True)
            error_label.setStyleSheet(
                "color: #e7b76a; font-size: 11px;"
            )
            layout.addWidget(error_label)

        tools_title = QLabel(
            "Herramientas"
        )

        tools_title.setStyleSheet(
            """
            color: #8b9098;
            font-size: 10px;
            font-weight: bold;
            """
        )

        layout.addWidget(
            tools_title
        )

        tools = plugin.get(
            "tools",
            []
        )

        if tools:
            for tool in tools:
                row = PluginToolRow(
                    tool
                )

                layout.addWidget(
                    row
                )

        else:
            empty = QLabel(
                "Este plugin no tiene herramientas registradas."
            )

            empty.setStyleSheet(
                """
                color: #666b73;
                font-size: 11px;
                """
            )

            layout.addWidget(
                empty
            )


class PluginsWidget(QWidget):
    def __init__(
        self,
        plugin_manager,
        plugin_config,
        parent=None,
    ):
        super().__init__(parent)

        self.plugins = plugin_manager
        self.config = plugin_config

        self._build_ui()

    def _build_ui(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: #101114;
                color: #eeeeee;
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

        root_layout = QVBoxLayout(
            self
        )

        root_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.NoFrame
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            28,
            24,
            28,
            28,
        )

        content_layout.setSpacing(
            18
        )

        header = QHBoxLayout()

        title_layout = QVBoxLayout()

        title_layout.setSpacing(
            4
        )

        title = QLabel(
            "Plugins"
        )

        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)

        title.setFont(
            title_font
        )

        title.setStyleSheet(
            """
            color: #f2f2f2;
            """
        )

        subtitle = QLabel(
            "Integraciones y herramientas conectadas a Rebecca"
        )

        subtitle.setStyleSheet(
            """
            color: #747982;
            font-size: 12px;
            """
        )

        title_layout.addWidget(
            title
        )

        title_layout.addWidget(
            subtitle
        )

        header.addLayout(
            title_layout,
            1,
        )

        self.refresh_button = QPushButton(
            "Actualizar"
        )

        self.refresh_button.setMinimumHeight(
            38
        )

        self.refresh_button.setMinimumWidth(
            100
        )

        self.refresh_button.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #30343a;
                border-radius: 9px;
                background-color: #1b1e23;
                color: #d8dadd;
                font-size: 12px;
                padding: 0 14px;
            }

            QPushButton:hover {
                background-color: #252930;
                color: #ffffff;
            }

            QPushButton:pressed {
                background-color: #2c3138;
            }
            """
        )

        self.refresh_button.clicked.connect(
            self.refresh_plugins
        )

        header.addWidget(
            self.refresh_button
        )

        content_layout.addLayout(
            header
        )

        self.plugin_container = QVBoxLayout()

        self.plugin_container.setSpacing(
            12
        )

        content_layout.addLayout(
            self.plugin_container
        )

        content_layout.addStretch()

        scroll.setWidget(
            content
        )

        root_layout.addWidget(
            scroll
        )

        self.refresh_plugins()

    def refresh_plugins(self):
        while (
            self.plugin_container.count()
            > 0
        ):
            item = (
                self.plugin_container.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        plugins = self.plugins.describe_plugins()

        if not plugins:
            empty = QLabel(
                "No hay plugins cargados."
            )

            empty.setStyleSheet(
                """
                color: #747982;
                font-size: 12px;
                padding: 20px;
                """
            )

            self.plugin_container.addWidget(
                empty
            )

            return

        for plugin in plugins:
            card = PluginCard(
                plugin,
                self.config,
                self.plugins,
            )

            self.plugin_container.addWidget(
                card
            )

