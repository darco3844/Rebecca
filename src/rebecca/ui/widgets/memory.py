from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class MemoryCard(QFrame):
    def __init__(
        self,
        memory,
        delete_callback,
        parent=None,
    ):
        super().__init__(parent)

        self.memory = memory
        self.delete_callback = delete_callback

        (
            memory_id,
            content,
            memory_type,
            importance,
            created_at,
            memory_key,
            memory_level,
        ) = memory

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
            9
        )

        header = QHBoxLayout()

        type_label = QLabel(
            str(memory_type)
        )

        type_label.setStyleSheet(
            """
            color: #78e0a0;
            background-color: #1d3428;
            border-radius: 7px;
            padding: 5px 8px;
            font-size: 10px;
            font-weight: bold;
            """
        )

        header.addWidget(
            type_label
        )

        level_label = QLabel(
            str(memory_level)
        )

        level_label.setStyleSheet(
            """
            color: #9ba1aa;
            background-color: #20242a;
            border-radius: 7px;
            padding: 5px 8px;
            font-size: 10px;
            """
        )

        header.addWidget(
            level_label
        )

        header.addStretch()

        importance_label = QLabel(
            f"Importancia {importance}/10"
        )

        importance_label.setStyleSheet(
            """
            color: #9ba1aa;
            font-size: 10px;
            """
        )

        header.addWidget(
            importance_label
        )

        layout.addLayout(
            header
        )

        content_label = QLabel(
            str(content)
        )

        content_label.setWordWrap(
            True
        )

        content_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        content_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Minimum,
        )

        content_label.setStyleSheet(
            """
            color: #eeeeee;
            font-size: 13px;
            """
        )

        layout.addWidget(
            content_label
        )

        footer = QHBoxLayout()

        date_label = QLabel(
            str(created_at)
        )

        date_label.setStyleSheet(
            """
            color: #60656d;
            font-size: 10px;
            """
        )

        footer.addWidget(
            date_label
        )

        if memory_key:
            key_label = QLabel(
                f"Clave: {memory_key}"
            )

            key_label.setStyleSheet(
                """
                color: #60656d;
                font-size: 10px;
                """
            )

            footer.addWidget(
                key_label
            )

        footer.addStretch()

        delete_button = QPushButton(
            "Eliminar"
        )

        delete_button.setCursor(
            Qt.PointingHandCursor
        )

        delete_button.setMinimumHeight(
            30
        )

        delete_button.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #493034;
                border-radius: 7px;
                background-color: #21181a;
                color: #d88989;
                font-size: 10px;
                padding: 0 10px;
            }

            QPushButton:hover {
                background-color: #352023;
                color: #f0a0a0;
            }

            QPushButton:pressed {
                background-color: #422629;
            }
            """
        )

        delete_button.clicked.connect(
            lambda: self.delete_callback(
                memory_id
            )
        )

        footer.addWidget(
            delete_button
        )

        layout.addLayout(
            footer
        )


class MemoryWidget(QWidget):
    def __init__(
        self,
        memory_manager,
        parent=None,
    ):
        super().__init__(parent)

        self.memory = memory_manager

        self._build_ui()

        self.refresh_memories()

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
            "Memoria"
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
            "Recuerdos persistentes que Rebecca ha almacenado"
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

        self.count_label = QLabel(
            "0 recuerdos"
        )

        self.count_label.setStyleSheet(
            """
            color: #8c929b;
            font-size: 11px;
            padding-right: 8px;
            """
        )

        header.addWidget(
            self.count_label
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
            self.refresh_memories
        )

        header.addWidget(
            self.refresh_button
        )

        content_layout.addLayout(
            header
        )

        search_frame = QFrame()

        search_frame.setStyleSheet(
            """
            QFrame {
                background-color: #17191d;
                border: 1px solid #292d33;
                border-radius: 12px;
            }
            """
        )

        search_layout = QHBoxLayout(
            search_frame
        )

        search_layout.setContentsMargins(
            10,
            7,
            7,
            7,
        )

        search_layout.setSpacing(
            8
        )

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Buscar en la memoria..."
        )

        self.search_input.setMinimumHeight(
            38
        )

        self.search_input.setStyleSheet(
            """
            QLineEdit {
                border: none;
                background: transparent;
                color: #eeeeee;
                font-size: 13px;
                padding: 5px;
            }
            """
        )

        self.search_input.returnPressed.connect(
            self.search_memories
        )

        search_layout.addWidget(
            self.search_input,
            1,
        )

        self.search_button = QPushButton(
            "Buscar"
        )

        self.search_button.setMinimumHeight(
            36
        )

        self.search_button.setMinimumWidth(
            80
        )

        self.search_button.setStyleSheet(
            """
            QPushButton {
                border: none;
                border-radius: 8px;
                background-color: #315f9f;
                color: white;
                font-size: 11px;
                font-weight: bold;
                padding: 0 12px;
            }

            QPushButton:hover {
                background-color: #3c70b8;
            }

            QPushButton:pressed {
                background-color: #284e84;
            }
            """
        )

        self.search_button.clicked.connect(
            self.search_memories
        )

        search_layout.addWidget(
            self.search_button
        )

        content_layout.addWidget(
            search_frame
        )

        self.results_label = QLabel(
            "Recuerdos recientes"
        )

        self.results_label.setStyleSheet(
            """
            color: #8b9098;
            font-size: 11px;
            font-weight: bold;
            """
        )

        content_layout.addWidget(
            self.results_label
        )

        self.memory_container = QVBoxLayout()

        self.memory_container.setSpacing(
            10
        )

        content_layout.addLayout(
            self.memory_container
        )

        content_layout.addStretch()

        scroll.setWidget(
            content
        )

        root_layout.addWidget(
            scroll
        )

    def _clear_memories(self):
        while (
            self.memory_container.count()
            > 0
        ):
            item = (
                self.memory_container.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    def refresh_memories(self):
        self.search_input.clear()

        self.results_label.setText(
            "Recuerdos recientes"
        )

        try:
            count = self.memory.count()

            self.count_label.setText(
                f"{count} recuerdos"
            )

            memories = self.memory.recent(
                limit=100
            )

            self._show_memories(
                memories
            )

        except Exception as error:
            self._show_error(
                error
            )

    def search_memories(self):
        text = (
            self.search_input.text()
            .strip()
        )

        if not text:
            self.refresh_memories()
            return

        try:
            memories = self.memory.search(
                text,
                limit=100,
            )

            self.results_label.setText(
                f"Resultados para: {text}"
            )

            self._show_memories(
                memories
            )

        except Exception as error:
            self._show_error(
                error
            )

    def _show_memories(
        self,
        memories,
    ):
        self._clear_memories()

        if not memories:
            empty = QLabel(
                "No hay recuerdos que mostrar."
            )

            empty.setAlignment(
                Qt.AlignCenter
            )

            empty.setStyleSheet(
                """
                color: #666b73;
                font-size: 12px;
                padding: 30px;
                """
            )

            self.memory_container.addWidget(
                empty
            )

            return

        for memory in memories:
            card = MemoryCard(
                memory,
                self.delete_memory,
            )

            self.memory_container.addWidget(
                card
            )

    def _show_error(
        self,
        error,
    ):
        self._clear_memories()

        self.count_label.setText(
            "Error"
        )

        label = QLabel(
            f"No se pudo cargar la memoria:\n{error}"
        )

        label.setWordWrap(
            True
        )

        label.setStyleSheet(
            """
            color: #f08080;
            font-size: 12px;
            padding: 20px;
            """
        )

        self.memory_container.addWidget(
            label
        )

    def delete_memory(
        self,
        memory_id,
    ):
        memory = self.memory.get_memory(
            memory_id
        )

        if memory is None:
            return

        content = str(
            memory[1]
        )

        confirmation = QMessageBox.question(
            self,
            "Eliminar memoria",
            (
                "¿Eliminar este recuerdo?\n\n"
                f"{content}"
            ),
            QMessageBox.Yes
            | QMessageBox.No,
            QMessageBox.No,
        )

        if confirmation != QMessageBox.Yes:
            return

        try:
            self.memory.forget(
                memory_id
            )

            self.refresh_memories()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo eliminar la memoria:\n{error}",
            )

