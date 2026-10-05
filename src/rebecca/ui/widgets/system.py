from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class SystemCard(QFrame):
    def __init__(
        self,
        title,
        parent=None,
    ):
        super().__init__(parent)

        self.setMinimumHeight(
            115
        )

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

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
            16,
            14,
            16,
            14,
        )

        layout.setSpacing(
            7
        )

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet(
            """
            color: #7d838c;
            font-size: 11px;
            font-weight: bold;
            """
        )

        self.value_label = QLabel(
            "Cargando..."
        )

        value_font = QFont()
        value_font.setPointSize(14)
        value_font.setBold(True)

        self.value_label.setFont(
            value_font
        )

        self.value_label.setWordWrap(
            True
        )

        self.value_label.setStyleSheet(
            """
            color: #eeeeee;
            """
        )

        layout.addWidget(
            title_label
        )

        layout.addWidget(
            self.value_label
        )

        layout.addStretch()

    def set_value(
        self,
        value,
    ):
        self.value_label.setText(
            str(value)
        )


class SystemWidget(QWidget):
    def __init__(
        self,
        tool_manager,
        parent=None,
    ):
        super().__init__(parent)

        self.tools = tool_manager

        self._build_ui()

        self.refresh_data()

        self.timer = QTimer(
            self
        )

        self.timer.timeout.connect(
            self.refresh_data
        )

        self.timer.start(
            10000
        )

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

        root_layout.setSpacing(
            0
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
            20
        )

        header_layout = QHBoxLayout()

        title_container = QVBoxLayout()

        title_container.setSpacing(
            4
        )

        title = QLabel(
            "Sistema"
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
            "Estado y recursos del equipo"
        )

        subtitle.setStyleSheet(
            """
            color: #747982;
            font-size: 12px;
            """
        )

        title_container.addWidget(
            title
        )

        title_container.addWidget(
            subtitle
        )

        header_layout.addLayout(
            title_container
        )

        header_layout.addStretch()

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
            self.refresh_data
        )

        header_layout.addWidget(
            self.refresh_button
        )

        content_layout.addLayout(
            header_layout
        )

        grid = QGridLayout()

        grid.setSpacing(
            12
        )

        self.os_card = SystemCard(
            "SISTEMA OPERATIVO"
        )

        self.kernel_card = SystemCard(
            "KERNEL"
        )

        self.architecture_card = SystemCard(
            "ARQUITECTURA"
        )

        self.cpu_card = SystemCard(
            "PROCESADOR"
        )

        self.cores_card = SystemCard(
            "NÚCLEOS LÓGICOS"
        )

        self.disk_card = SystemCard(
            "ALMACENAMIENTO"
        )

        self.disk_usage_card = SystemCard(
            "USO DEL DISCO"
        )

        self.processes_card = SystemCard(
            "PROCESOS ACTIVOS"
        )

        grid.addWidget(
            self.os_card,
            0,
            0,
        )

        grid.addWidget(
            self.kernel_card,
            0,
            1,
        )

        grid.addWidget(
            self.architecture_card,
            1,
            0,
        )

        grid.addWidget(
            self.cpu_card,
            1,
            1,
        )

        grid.addWidget(
            self.cores_card,
            2,
            0,
        )

        grid.addWidget(
            self.disk_card,
            2,
            1,
        )

        grid.addWidget(
            self.disk_usage_card,
            3,
            0,
        )

        grid.addWidget(
            self.processes_card,
            3,
            1,
        )

        content_layout.addLayout(
            grid
        )

        content_layout.addStretch()

        scroll.setWidget(
            content
        )

        root_layout.addWidget(
            scroll
        )

    def _run_tool(
        self,
        name,
    ):
        return self.tools.run(
            name,
            max_permission="read",
        )

    def refresh_data(self):
        try:
            system = self._run_tool(
                "system_info"
            )

            cpu = self._run_tool(
                "cpu_info"
            )

            disk = self._run_tool(
                "disk_info"
            )

            processes = self._run_tool(
                "process_info"
            )

            if "error" not in system:
                self.os_card.set_value(
                    system.get(
                        "distribution",
                        "Desconocido",
                    )
                )

                self.kernel_card.set_value(
                    system.get(
                        "kernel",
                        "Desconocido",
                    )
                )

                self.architecture_card.set_value(
                    system.get(
                        "architecture",
                        "Desconocido",
                    )
                )

                self.cores_card.set_value(
                    system.get(
                        "logical_cpus",
                        "Desconocido",
                    )
                )

            else:
                self.os_card.set_value(
                    "Error"
                )

            if "error" not in cpu:
                self.cpu_card.set_value(
                    cpu.get(
                        "model",
                        "Desconocido",
                    )
                )

            else:
                self.cpu_card.set_value(
                    "Error"
                )

            if "error" not in disk:
                total = disk.get(
                    "total_gb",
                    0,
                )

                used = disk.get(
                    "used_gb",
                    0,
                )

                free = disk.get(
                    "free_gb",
                    0,
                )

                usage = disk.get(
                    "used_percent",
                    0,
                )

                self.disk_card.set_value(
                    f"{total} GB totales"
                )

                self.disk_usage_card.set_value(
                    f"{used} GB usados · "
                    f"{free} GB libres · "
                    f"{usage}%"
                )

            else:
                self.disk_card.set_value(
                    "Error"
                )

                self.disk_usage_card.set_value(
                    "Error"
                )

            if "error" not in processes:
                count = processes.get(
                    "count",
                    0,
                )

                self.processes_card.set_value(
                    f"{count} procesos"
                )

            else:
                self.processes_card.set_value(
                    "Error"
                )

        except Exception as error:
            self.os_card.set_value(
                f"Error: {error}"
            )

