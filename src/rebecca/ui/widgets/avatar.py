from math import sin, cos, pi

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QRadialGradient, QPen
from PySide6.QtWidgets import QWidget


class AvatarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state = "idle"
        self.phase = 0.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(33)

        self.setMinimumSize(90, 90)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def set_state(self, state):
        if state not in {"idle", "thinking", "speaking", "tool", "error", "offline"}:
            state = "idle"
        self.state = state
        self.update()

    def _animate(self):
        speed = {
            "idle": 0.012,
            "thinking": 0.030,
            "speaking": 0.060,
            "tool": 0.045,
            "error": 0.080,
            "offline": 0.002,
        }.get(self.state, 0.012)

        self.phase = (self.phase + speed) % (pi * 2)
        self.update()

    def paintEvent(self, event):
        del event

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() / 2
        cy = self.height() / 2
        radius = min(self.width(), self.height()) * 0.43

        self._draw_glow(painter, cx, cy, radius)
        self._draw_orb(painter, cx, cy, radius)

    def _draw_glow(self, painter, cx, cy, radius):
        if self.state == "offline":
            return

        pulse = (sin(self.phase) + 1) / 2
        r = radius * (1.05 + pulse * 0.12)

        gradient = QRadialGradient(cx, cy, r)

        gradient.setColorAt(
            0.0,
            QColor(99, 245, 168, 45),
        )
        gradient.setColorAt(
            0.55,
            QColor(155, 107, 255, 28),
        )
        gradient.setColorAt(
            1.0,
            QColor(155, 107, 255, 0),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawEllipse(
            int(cx - r),
            int(cy - r),
            int(r * 2),
            int(r * 2),
        )

    def _draw_orb(self, painter, cx, cy, radius):
        if self.state == "offline":
            green = QColor(75, 100, 88, 235)
            purple = QColor(75, 65, 100, 235)
        elif self.state == "error":
            green = QColor(255, 75, 145, 245)
            purple = QColor(180, 70, 255, 245)
        else:
            green = QColor(75, 245, 160, 250)
            purple = QColor(155, 90, 255, 250)

        orb = QPainterPath()
        orb.addEllipse(
            int(cx - radius),
            int(cy - radius),
            int(radius * 2),
            int(radius * 2),
        )

        painter.save()
        painter.setClipPath(orb)

        gradient = QRadialGradient(
            cx - radius * 0.20,
            cy - radius * 0.30,
            radius * 1.35,
        )

        gradient.setColorAt(
            0.0,
            QColor(220, 255, 238, 245),
        )
        gradient.setColorAt(
            0.25,
            green,
        )
        gradient.setColorAt(
            0.58,
            QColor(
                90,
                205,
                190,
                245,
            ),
        )
        gradient.setColorAt(
            0.82,
            purple,
        )
        gradient.setColorAt(
            1.0,
            QColor(70, 35, 115, 245),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawEllipse(
            int(cx - radius),
            int(cy - radius),
            int(radius * 2),
            int(radius * 2),
        )

        self._draw_waves(
            painter,
            cx,
            cy,
            radius,
            green,
            purple,
        )

        painter.restore()

    def _draw_waves(
        self,
        painter,
        cx,
        cy,
        radius,
        green,
        purple,
    ):
        for i in range(11):
            path = QPainterPath()

            y0 = (
                cy
                - radius * 0.82
                + i * radius * 0.165
            )

            amplitude = radius * (
                0.025 + i * 0.002
            )

            frequency = 1.5 + i * 0.11
            phase = (
                self.phase * (0.55 + i * 0.035)
                + i * 0.65
            )

            for step in range(81):
                t = step / 80
                x = (
                    cx
                    - radius * 1.15
                    + t * radius * 2.30
                )

                y = y0 + sin(
                    t * pi * frequency + phase
                ) * amplitude

                if step == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)

            color = QColor(
                green if i % 2 == 0 else purple
            )
            color.setAlpha(35 + i * 4)

            pen = QPen(color)
            pen.setWidthF(max(1.0, radius * 0.012))

            painter.setPen(pen)
            painter.drawPath(path)

        shine = QRadialGradient(
            cx - radius * 0.22,
            cy - radius * 0.30,
            radius * 0.75,
        )

        shine.setColorAt(
            0.0,
            QColor(245, 255, 250, 70),
        )
        shine.setColorAt(
            0.45,
            QColor(150, 255, 205, 20),
        )
        shine.setColorAt(
            1.0,
            QColor(150, 255, 205, 0),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(shine)

        painter.drawEllipse(
            int(cx - radius * 0.9),
            int(cy - radius * 0.9),
            int(radius * 1.8),
            int(radius * 1.8),
        )
