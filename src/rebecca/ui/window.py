from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
    Slot,
)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.rebecca.ui.widgets.chat import (
    ChatWidget,
)

from src.rebecca.ui.widgets.sidebar import (
    SidebarWidget,
)

from src.rebecca.ui.widgets.memory import (
    MemoryWidget,
)

from src.rebecca.ui.widgets.system import (
    SystemWidget,
)

from src.rebecca.ui.widgets.plugins import (
    PluginsWidget,
)

from src.rebecca.ui.widgets.avatar import (
    AvatarWidget,
)


class ResponseWorker(QObject):
    finished = Signal(str)
    failed = Signal(str)

    def __init__(
        self,
        engine,
        message,
    ):
        super().__init__()

        self.engine = engine
        self.message = message

    @Slot()
    def run(self):
        try:
            response = self.engine.respond(
                self.message
            )

            self.finished.emit(
                str(response)
            )

        except Exception as error:
            self.failed.emit(
                str(error)
            )


class ChatWindow(QMainWindow):
    def __init__(
        self,
        engine,
    ):
        super().__init__()

        self.engine = engine

        self.thread = None
        self.worker = None

        self.setWindowTitle(
            "Rebecca"
        )

        self.resize(
            1100,
            700,
        )

        self.setMinimumSize(
            850,
            550,
        )

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        central = QWidget()

        self.setCentralWidget(
            central
        )

        central.setStyleSheet(
            """
            QWidget {
                background-color: #101114;
                color: #eeeeee;
            }
            """
        )

        main_layout = QHBoxLayout(
            central
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        main_layout.setSpacing(
            0
        )

        self.sidebar = SidebarWidget()

        main_layout.addWidget(
            self.sidebar
        )

        content = QWidget()

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        content_layout.setSpacing(
            0
        )

        header = self._create_header()

        content_layout.addWidget(
            header
        )

        self.pages = QStackedWidget()

        self.chat = ChatWidget()

        self.pages.addWidget(
            self.chat
        )

        self.memory = MemoryWidget(
            self.engine.memory
        )

        self.pages.addWidget(
            self.memory
        )

        self.system = SystemWidget(
            self.engine.tools
        )

        self.pages.addWidget(
            self.system
        )

        self.plugins = PluginsWidget(
            self.engine.plugins,
            self.engine.plugin_config,
        )

        self.pages.addWidget(
            self.plugins
        )

        content_layout.addWidget(
            self.pages,
            1,
        )

        main_layout.addWidget(
            content,
            1,
        )

        self.chat.add_message(
            "Rebecca",
            "Sistema iniciado. Estoy lista.",
        )

    def _create_header(self):
        header = QFrame()

        header.setFixedHeight(
            72
        )

        header.setStyleSheet(
            """
            QFrame {
                background-color: #15171a;
                border-bottom: 1px solid #292c31;
            }
            """
        )

        layout = QHBoxLayout(
            header
        )

        layout.setContentsMargins(
            22,
            10,
            22,
            10,
        )

        layout.setSpacing(
            12
        )

        self.avatar = AvatarWidget(
            header
        )

        self.avatar.setFixedSize(
            52,
            52
        )

        layout.addWidget(
            self.avatar
        )

        title = QLabel(
            "Rebecca"
        )

        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setBold(True)

        title.setFont(
            title_font
        )

        title.setStyleSheet(
            """
            color: #f2f2f2;
            """
        )

        layout.addWidget(
            title
        )

        layout.addStretch()

        self.header_status = QLabel(
            "● En línea"
        )

        self.header_status.setStyleSheet(
            """
            color: #6ee7a8;
            font-size: 11px;
            """
        )

        layout.addWidget(
            self.header_status
        )

        return header

    def _connect_signals(self):
        self.chat.input.returnPressed.connect(
            self.send_message
        )

        self.chat.send_button.clicked.connect(
            self.send_message
        )

        self.sidebar.navigation_requested.connect(
            self._handle_navigation
        )

    def send_message(self):
        if self.thread is not None:
            return

        message = (
            self.chat.get_input_text()
        )

        if not message:
            return

        self.chat.clear_input()

        self.chat.add_message(
            "Tú",
            message,
        )

        self._set_thinking_state()

        self.chat.set_input_enabled(
            False
        )

        self.pages.setCurrentWidget(
            self.chat
        )

        self.thread = QThread()

        self.worker = ResponseWorker(
            self.engine,
            message,
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.finished.connect(
            self._response_finished
        )

        self.worker.failed.connect(
            self._response_failed
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.failed.connect(
            self.thread.quit
        )

        self.thread.finished.connect(
            self._thread_finished
        )

        self.thread.start()

    def _set_thinking_state(self):
        self.sidebar.avatar.set_state("thinking")

        self.header_status.setText(
            "● Rebecca está pensando..."
        )

        self.header_status.setStyleSheet(
            """
            color: #f6c85f;
            font-size: 11px;
            """
        )

    @Slot(str)
    def _response_finished(
        self,
        response,
    ):
        self.chat.add_message(
            "Rebecca",
            response,
        )

        self._set_online_state()

    @Slot(str)
    def _response_failed(
        self,
        error,
    ):
        self.chat.add_message(
            "Rebecca",
            f"Error: {error}",
        )

        self.sidebar.avatar.set_state("error")

        self.header_status.setText(
            "● Error"
        )

        self.header_status.setStyleSheet(
            """
            color: #f87171;
            font-size: 11px;
            """
        )

    def _set_online_state(self):
        self.sidebar.avatar.set_state("idle")

        self.header_status.setText(
            "● En línea"
        )

        self.header_status.setStyleSheet(
            """
            color: #6ee7a8;
            font-size: 11px;
            """
        )

    def _handle_navigation(
        self,
        destination,
    ):
        if destination == "new_chat":
            self._new_chat()

        elif destination == "memory":
            self.pages.setCurrentWidget(
                self.memory
            )

            self.memory.refresh_memories()

        elif destination == "system":
            self.pages.setCurrentWidget(
                self.system
            )

        elif destination == "plugins":
            self.pages.setCurrentWidget(
                self.plugins
            )

            self.plugins.refresh_plugins()

        elif destination == "tools":
            self._show_placeholder(
                "Herramientas"
            )

        elif destination == "settings":
            self._show_placeholder(
                "Configuración"
            )

    def _new_chat(self):
        self.pages.setCurrentWidget(
            self.chat
        )

        while (
            self.chat.chat_layout.count()
            > 1
        ):
            item = (
                self.chat.chat_layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self.chat.add_message(
            "Rebecca",
            "Nueva conversación iniciada.",
        )

    def _show_placeholder(
        self,
        name,
    ):
        self.pages.setCurrentWidget(
            self.chat
        )

        self.chat.add_message(
            "Rebecca",
            (
                f"El panel de {name} todavía está "
                "en construcción."
            ),
        )

    def _thread_finished(self):
        if self.worker is not None:
            self.worker.deleteLater()

        if self.thread is not None:
            self.thread.deleteLater()

        self.worker = None
        self.thread = None

        self.chat.set_input_enabled(
            True
        )

        self.chat.input.setFocus()

    def closeEvent(
        self,
        event,
    ):
        if self.thread is not None:
            self.thread.quit()

            self.thread.wait(
                2000
            )

        event.accept()

