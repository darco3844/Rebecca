from math import cos, pi, sin

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QRadialGradient,
    QPen,
)
from PySide6.QtWidgets import QWidget


class AvatarWidget(QWidget):
    """
    //:: d4RCO • 3844 :://

    Avatar visual de Rebecca.

    Estados:
        idle      -> respiración suave
        thinking  -> pulso de procesamiento
        speaking  -> actividad intensa
        tool      -> energía circulando
        error     -> pulso de error
        offline   -> estado atenuado
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.state = "idle"
        self.phase = 0.0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(33)

        self.setMinimumSize(90, 90)
        self.setAttribute(Qt.WA_TranslucentBackground)

    # ---------------------------------------------------------
    # STATE
    # ---------------------------------------------------------

    def set_state(self, state):
        if state not in {
            "idle",
            "thinking",
            "speaking",
            "tool",
            "error",
            "offline",
        }:
            state = "idle"

        self.state = state
        self.update()

    # ---------------------------------------------------------
    # ANIMATION
    # ---------------------------------------------------------

    def _animate(self):
        speed = {
            "idle": 0.018,
            "thinking": 0.038,
            "speaking": 0.065,
            "tool": 0.052,
            "error": 0.090,
            "offline": 0.002,
        }.get(self.state, 0.018)

        self.phase = (self.phase + speed) % (pi * 2)
        self.update()

    # ---------------------------------------------------------
    # PAINT
    # ---------------------------------------------------------

    def paintEvent(self, event):
        del event

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx = self.width() / 2
        cy = self.height() / 2

        base_radius = min(
            self.width(),
            self.height(),
        ) * 0.43

        radius = self._animated_radius(base_radius)

        self._draw_glow(
            painter,
            cx,
            cy,
            radius,
        )

        self._draw_orb(
            painter,
            cx,
            cy,
            radius,
        )

    # ---------------------------------------------------------
    # RADIUS / BREATHING
    # ---------------------------------------------------------

    def _animated_radius(self, radius):
        if self.state == "offline":
            return radius

        if self.state == "idle":
            # Respiración muy suave.
            pulse = sin(self.phase) * 0.018
            return radius * (1.0 + pulse)

        if self.state == "thinking":
            # Pulso perceptible de procesamiento.
            pulse = (sin(self.phase) + 1.0) / 2.0
            return radius * (1.0 + pulse * 0.045)

        if self.state == "speaking":
            # Expansión más marcada.
            pulse = (sin(self.phase * 1.35) + 1.0) / 2.0
            return radius * (1.0 + pulse * 0.075)

        if self.state == "tool":
            # Movimiento energético irregular.
            pulse = (
                sin(self.phase * 1.7)
                + sin(self.phase * 2.9) * 0.35
            )
            return radius * (1.0 + pulse * 0.035)

        if self.state == "error":
            # Pulso rápido.
            pulse = (sin(self.phase * 2.2) + 1.0) / 2.0
            return radius * (1.0 + pulse * 0.055)

        return radius

    # ---------------------------------------------------------
    # GLOW
    # ---------------------------------------------------------

    def _draw_glow(self, painter, cx, cy, radius):
        if self.state == "offline":
            return

        pulse = (sin(self.phase) + 1.0) / 2.0

        if self.state == "thinking":
            glow_scale = 1.12 + pulse * 0.20

        elif self.state == "speaking":
            glow_scale = 1.16 + pulse * 0.28

        elif self.state == "tool":
            glow_scale = 1.14 + pulse * 0.24

        elif self.state == "error":
            glow_scale = 1.10 + pulse * 0.22

        else:
            glow_scale = 1.05 + pulse * 0.10

        r = radius * glow_scale

        gradient = QRadialGradient(
            cx,
            cy,
            r,
        )

        if self.state == "error":
            gradient.setColorAt(
                0.0,
                QColor(255, 70, 150, 60),
            )
            gradient.setColorAt(
                0.55,
                QColor(180, 70, 255, 30),
            )
        else:
            gradient.setColorAt(
                0.0,
                QColor(99, 245, 168, 55),
            )
            gradient.setColorAt(
                0.55,
                QColor(155, 107, 255, 32),
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

    # ---------------------------------------------------------
    # ORB
    # ---------------------------------------------------------

    def _draw_orb(
        self,
        painter,
        cx,
        cy,
        radius,
    ):
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
            QColor(
                70,
                35,
                115,
                245,
            ),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)

        painter.drawEllipse(
            int(cx - radius),
            int(cy - radius),
            int(radius * 2),
            int(radius * 2),
        )

        self._draw_energy(
            painter,
            cx,
            cy,
            radius,
            green,
            purple,
        )

        self._draw_shine(
            painter,
            cx,
            cy,
            radius,
        )

        painter.restore()

    # ---------------------------------------------------------
    # ENERGY WAVES
    # ---------------------------------------------------------

    def _draw_energy(
        self,
        painter,
        cx,
        cy,
        radius,
        green,
        purple,
    ):
        if self.state == "offline":
            return

        wave_count = 11

        for i in range(wave_count):
            path = QPainterPath()

            y0 = (
                cy
                - radius * 0.82
                + i * radius * 0.165
            )

            # Las ondas reaccionan al estado.
            if self.state == "idle":
                amplitude = radius * (
                    0.018 + i * 0.001
                )

                movement = 0.45

            elif self.state == "thinking":
                amplitude = radius * (
                    0.028 + i * 0.0025
                )

                movement = 0.85

            elif self.state == "speaking":
                amplitude = radius * (
                    0.040 + i * 0.003
                )

                movement = 1.25

            elif self.state == "tool":
                amplitude = radius * (
                    0.050 + i * 0.0035
                )

                movement = 1.55

            elif self.state == "error":
                amplitude = radius * (
                    0.035 + i * 0.002
                )

                movement = 1.75

            else:
                amplitude = radius * 0.02
                movement = 0.2

            frequency = 1.5 + i * 0.11

            phase = (
                self.phase * (
                    movement + i * 0.025
                )
                + i * 0.65
            )

            for step in range(81):
                t = step / 80

                x = (
                    cx
                    - radius * 1.15
                    + t * radius * 2.30
                )

                y = (
                    y0
                    + sin(
                        t * pi * frequency
                        + phase
                    ) * amplitude
                )

                if step == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)

            color = QColor(
                green
                if i % 2 == 0
                else purple
            )

            if self.state == "thinking":
                alpha = 45 + i * 5

            elif self.state == "speaking":
                alpha = 55 + i * 5

            elif self.state == "tool":
                alpha = 65 + i * 6

            elif self.state == "error":
                alpha = 50 + i * 4

            else:
                alpha = 35 + i * 4

            color.setAlpha(
                min(alpha, 130)
            )

            pen = QPen(color)

            pen.setWidthF(
                max(
                    1.0,
                    radius * 0.012,
                )
            )

            painter.setPen(pen)
            painter.drawPath(path)

        # Núcleo energético adicional.
        if self.state in {
            "thinking",
            "speaking",
            "tool",
        }:
            self._draw_energy_core(
                painter,
                cx,
                cy,
                radius,
                green,
                purple,
            )

    # ---------------------------------------------------------
    # ENERGY CORE
    # ---------------------------------------------------------

    def _draw_energy_core(
        self,
        painter,
        cx,
        cy,
        radius,
        green,
        purple,
    ):
        intensity = (
            sin(self.phase * 1.8)
            + 1.0
        ) / 2.0

        core_radius = radius * (
            0.10 + intensity * 0.045
        )

        gradient = QRadialGradient(
            cx,
            cy,
            core_radius * 2.5,
        )

        gradient.setColorAt(
            0.0,
            QColor(
                245,
                255,
                250,
                115,
            ),
        )

        gradient.setColorAt(
            0.30,
            QColor(
                green.red(),
                green.green(),
                green.blue(),
                65,
            ),
        )

        gradient.setColorAt(
            0.70,
            QColor(
                purple.red(),
                purple.green(),
                purple.blue(),
                25,
            ),
        )

        gradient.setColorAt(
            1.0,
            QColor(
                purple.red(),
                purple.green(),
                purple.blue(),
                0,
            ),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)

        painter.drawEllipse(
            int(
                cx - core_radius * 2.5
            ),
            int(
                cy - core_radius * 2.5
            ),
            int(
                core_radius * 5.0
            ),
            int(
                core_radius * 5.0
            ),
        )

    # ---------------------------------------------------------
    # SHINE
    # ---------------------------------------------------------

    def _draw_shine(
        self,
        painter,
        cx,
        cy,
        radius,
    ):
        intensity = (
            sin(self.phase)
            + 1.0
        ) / 2.0

        shine = QRadialGradient(
            cx - radius * 0.22,
            cy - radius * 0.30,
            radius * 0.75,
        )

        shine.setColorAt(
            0.0,
            QColor(
                245,
                255,
                250,
                65 + int(
                    intensity * 20
                ),
            ),
        )

        shine.setColorAt(
            0.45,
            QColor(
                150,
                255,
                205,
                20,
            ),
        )

        shine.setColorAt(
            1.0,
            QColor(
                150,
                255,
                205,
                0,
            ),
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(shine)

        painter.drawEllipse(
            int(
                cx - radius * 0.9
            ),
            int(
                cy - radius * 0.9
            ),
            int(
                radius * 1.8
            ),
            int(
                radius * 1.8
            ),
        )

