from math import cos, pi, sin

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QRadialGradient,
)
from PySide6.QtWidgets import QWidget


class AvatarWidget(QWidget):
    """Orb de Rebecca.

    Diseño:
    - energía líquida integrada
    - ondas orgánicas
    - verde + morado
    - render ligero mediante caché
    """

    VALID_STATES = {
        "idle",
        "thinking",
        "speaking",
        "tool",
        "error",
        "offline",
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self.state = "idle"
        self.phase = 0.0

        self._orb_cache = None
        self._glow_cache = None
        self._cache_size = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(33)

        self.setMinimumSize(90, 90)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def set_state(self, state):
        if state not in self.VALID_STATES:
            state = "idle"

        self.state = state
        self.update()

    def resizeEvent(self, event):
        self._orb_cache = None
        self._glow_cache = None
        self._cache_size = None
        super().resizeEvent(event)

    def _animate(self):
        speed = {
            "idle": 0.018,
            "thinking": 0.045,
            "speaking": 0.070,
            "tool": 0.055,
            "error": 0.090,
            "offline": 0.004,
        }.get(self.state, 0.018)

        self.phase = (
            self.phase + speed
        ) % (pi * 2)

        self.update()

    def paintEvent(self, event):
        del event

        self._ensure_cache()

        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.Antialiasing,
            True,
        )

        cx = self.width() * 0.5
        cy = self.height() * 0.5

        radius = min(
            self.width(),
            self.height(),
        ) * 0.36

        pulse = (
            sin(self.phase) + 1.0
        ) * 0.5

        breathing = {
            "idle": 1.8,
            "thinking": 4.0,
            "speaking": 6.0,
            "tool": 3.5,
            "error": 3.0,
            "offline": 0.0,
        }.get(self.state, 1.8)

        radius += (
            sin(self.phase)
            * breathing
        )

        self._draw_glow(
            painter,
            cx,
            cy,
            radius,
            pulse,
        )

        self._draw_liquid_orb(
            painter,
            cx,
            cy,
            radius,
        )

        painter.end()

    def _ensure_cache(self):
        size = (
            self.width(),
            self.height(),
        )

        if (
            self._orb_cache is not None
            and self._cache_size == size
        ):
            return

        self._cache_size = size

        width = self.width()
        height = self.height()

        cx = width * 0.5
        cy = height * 0.5
        radius = min(
            width,
            height,
        ) * 0.36

        self._orb_cache = self._create_orb_cache(
            width,
            height,
            cx,
            cy,
            radius,
        )

        self._glow_cache = self._create_glow_cache(
            width,
            height,
            cx,
            cy,
            radius,
        )

    def _create_orb_cache(
        self,
        width,
        height,
        cx,
        cy,
        radius,
    ):
        from PySide6.QtGui import QImage

        image = QImage(
            width,
            height,
            QImage.Format_ARGB32_Premultiplied,
        )

        image.fill(
            QColor(
                0,
                0,
                0,
                0,
            )
        )

        painter = QPainter(image)
        painter.setRenderHint(
            QPainter.Antialiasing,
            True,
        )

        orb = QPainterPath()

        orb.addEllipse(
            int(cx - radius),
            int(cy - radius),
            int(radius * 2),
            int(radius * 2),
        )

        painter.setClipPath(orb)

        gradient = QRadialGradient(
            cx - radius * 0.28,
            cy - radius * 0.35,
            radius * 1.55,
        )

        gradient.setColorAt(
            0.00,
            QColor(220, 255, 238, 255),
        )

        gradient.setColorAt(
            0.16,
            QColor(80, 235, 165, 255),
        )

        gradient.setColorAt(
            0.38,
            QColor(55, 205, 185, 255),
        )

        gradient.setColorAt(
            0.60,
            QColor(95, 155, 210, 255),
        )

        gradient.setColorAt(
            0.78,
            QColor(150, 80, 245, 255),
        )

        gradient.setColorAt(
            1.00,
            QColor(65, 30, 110, 255),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)

        painter.drawEllipse(
            int(cx - radius),
            int(cy - radius),
            int(radius * 2),
            int(radius * 2),
        )

        painter.end()

        return image

    def _create_glow_cache(
        self,
        width,
        height,
        cx,
        cy,
        radius,
    ):
        from PySide6.QtGui import QImage

        image = QImage(
            width,
            height,
            QImage.Format_ARGB32_Premultiplied,
        )

        image.fill(
            QColor(
                0,
                0,
                0,
                0,
            )
        )

        painter = QPainter(image)

        glow_radius = radius * 1.28

        gradient = QRadialGradient(
            cx,
            cy,
            glow_radius,
        )

        gradient.setColorAt(
            0.0,
            QColor(
                100,
                240,
                180,
                35,
            ),
        )

        gradient.setColorAt(
            0.45,
            QColor(
                150,
                90,
                255,
                20,
            ),
        )

        gradient.setColorAt(
            1.0,
            QColor(
                150,
                90,
                255,
                0,
            ),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)

        painter.drawEllipse(
            int(cx - glow_radius),
            int(cy - glow_radius),
            int(glow_radius * 2),
            int(glow_radius * 2),
        )

        painter.end()

        return image

    def _draw_glow(
        self,
        painter,
        cx,
        cy,
        radius,
        pulse,
    ):
        if (
            self.state == "offline"
            or self._glow_cache is None
        ):
            return

        painter.setOpacity(
            0.65 + pulse * 0.20
        )

        painter.drawImage(
            0,
            0,
            self._glow_cache,
        )

        painter.setOpacity(1.0)

    def _draw_liquid_orb(
        self,
        painter,
        cx,
        cy,
        radius,
    ):
        if self._orb_cache is None:
            return

        painter.drawImage(
            0,
            0,
            self._orb_cache,
        )

        orb = QPainterPath()

        orb.addEllipse(
            int(cx - radius),
            int(cy - radius),
            int(radius * 2),
            int(radius * 2),
        )

        painter.save()
        painter.setClipPath(orb)

        self._draw_liquid_wave(
            painter,
            cx,
            cy,
            radius,
            0,
        )

        self._draw_liquid_wave(
            painter,
            cx,
            cy,
            radius,
            1,
        )

        self._draw_liquid_wave(
            painter,
            cx,
            cy,
            radius,
            2,
        )

        painter.restore()

        self._draw_core(
            painter,
            cx,
            cy,
            radius,
        )

    def _draw_liquid_wave(
        self,
        painter,
        cx,
        cy,
        radius,
        index,
    ):
        phase = self.phase

        if index == 0:
            color = QColor(
                95,
                255,
                190,
                70,
            )

            offset = 0.0

        elif index == 1:
            color = QColor(
                185,
                105,
                255,
                65,
            )

            offset = 2.1

        else:
            color = QColor(
                70,
                235,
                210,
                48,
            )

            offset = 4.2

        drift = (
            phase * 0.65
            + offset
        )

        y = (
            cy
            + sin(drift)
            * radius
            * 0.24
        )

        amplitude = radius * 0.20

        path = QPainterPath()

        path.moveTo(
            cx - radius * 1.25,
            y,
        )

        path.cubicTo(
            cx - radius * 0.78,
            y - amplitude,
            cx - radius * 0.30,
            y + amplitude,
            cx + radius * 0.05,
            y,
        )

        path.cubicTo(
            cx + radius * 0.42,
            y - amplitude,
            cx + radius * 0.82,
            y + amplitude,
            cx + radius * 1.25,
            y,
        )

        path.lineTo(
            cx + radius * 1.25,
            cy + radius * 1.25,
        )

        path.lineTo(
            cx - radius * 1.25,
            cy + radius * 1.25,
        )

        path.closeSubpath()

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)

        painter.drawPath(path)

    def _draw_core(
        self,
        painter,
        cx,
        cy,
        radius,
    ):
        if self.state == "offline":
            return

        core = QRadialGradient(
            cx
            + cos(self.phase)
            * radius
            * 0.12,
            cy
            + sin(self.phase * 0.8)
            * radius
            * 0.10,
            radius * 0.42,
        )

        core.setColorAt(
            0.0,
            QColor(
                225,
                255,
                240,
                55,
            ),
        )

        core.setColorAt(
            0.45,
            QColor(
                100,
                245,
                190,
                22,
            ),
        )

        core.setColorAt(
            1.0,
            QColor(
                100,
                245,
                190,
                0,
            ),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(core)

        painter.drawEllipse(
            int(cx - radius * 0.42),
            int(cy - radius * 0.42),
            int(radius * 0.84),
            int(radius * 0.84),
        )
