from math import cos, sin, pi
from time import monotonic

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QRadialGradient, QPen
from PySide6.QtWidgets import QWidget


class OrbWidget(QWidget):
    IDLE = "idle"
    THINKING = "thinking"
    ACTIVE = "active"
    RESPONDING = "responding"

    def __init__(self, parent=None):
        super().__init__(parent)

        self._state = self.IDLE
        self._phase = 0.0
        self._started_at = monotonic()

        self.setAttribute(
            Qt.WA_TranslucentBackground,
            True,
        )

        self.setMinimumSize(
            52,
            52,
        )

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(16)

    @property
    def state(self):
        return self._state

    def set_state(self, state):
        if state not in {
            self.IDLE,
            self.THINKING,
            self.ACTIVE,
            self.RESPONDING,
        }:
            return

        self._state = state
        self._started_at = monotonic()
        self.update()

    def _animate(self):
        elapsed = monotonic() - self._started_at

        if self._state == self.IDLE:
            speed = 0.035

        elif self._state == self.THINKING:
            speed = 0.075

        elif self._state == self.ACTIVE:
            speed = 0.14

        else:
            speed = 0.10

        self._phase = elapsed * speed * 60.0

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing,
            True,
        )

        painter.setCompositionMode(
            QPainter.CompositionMode_SourceOver
        )

        center_x = self.width() / 2
        center_y = self.height() / 2

        base_radius = min(
            self.width(),
            self.height(),
        ) * 0.29

        if self._state == self.IDLE:
            pulse = sin(self._phase * 0.8) * 0.035
            radius = base_radius * (1.0 + pulse)
            halo_strength = 0.45

        elif self._state == self.THINKING:
            pulse = sin(self._phase * 1.7) * 0.075
            radius = base_radius * (1.0 + pulse)
            halo_strength = 0.65

        elif self._state == self.ACTIVE:
            pulse = sin(self._phase * 2.4) * 0.06
            radius = base_radius * (1.0 + pulse)
            halo_strength = 0.85

        else:
            elapsed = monotonic() - self._started_at
            response_pulse = max(
                0.0,
                1.0 - elapsed / 0.75,
            )

            radius = base_radius * (
                1.0 + response_pulse * 0.20
            )

            halo_strength = (
                0.55 + response_pulse * 0.35
            )

        self._draw_halo(
            painter,
            center_x,
            center_y,
            radius,
            halo_strength,
        )

        self._draw_orb(
            painter,
            center_x,
            center_y,
            radius,
        )

        if self._state in {
            self.THINKING,
            self.ACTIVE,
        }:
            self._draw_energy(
                painter,
                center_x,
                center_y,
                radius,
            )

        painter.end()

    def _draw_halo(
        self,
        painter,
        center_x,
        center_y,
        radius,
        strength,
    ):
        halo_radius = radius * 2.15

        gradient = QRadialGradient(
            center_x,
            center_y,
            halo_radius,
        )

        purple = QColor(
            150,
            82,
            255,
            int(70 * strength),
        )

        green = QColor(
            70,
            230,
            150,
            int(42 * strength),
        )

        gradient.setColorAt(
            0.0,
            QColor(
                150,
                82,
                255,
                int(38 * strength),
            ),
        )

        gradient.setColorAt(
            0.42,
            purple,
        )

        gradient.setColorAt(
            0.68,
            green,
        )

        gradient.setColorAt(
            1.0,
            QColor(
                0,
                0,
                0,
                0,
            ),
        )

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(
            center_x - halo_radius,
            center_y - halo_radius,
            halo_radius * 2,
            halo_radius * 2,
        )

    def _draw_orb(
        self,
        painter,
        center_x,
        center_y,
        radius,
    ):
        gradient = QRadialGradient(
            center_x - radius * 0.28,
            center_y - radius * 0.30,
            radius * 1.35,
        )

        gradient.setColorAt(
            0.0,
            QColor(
                222,
                190,
                255,
                255,
            ),
        )

        gradient.setColorAt(
            0.24,
            QColor(
                160,
                92,
                255,
                255,
            ),
        )

        gradient.setColorAt(
            0.62,
            QColor(
                104,
                53,
                190,
                255,
            ),
        )

        gradient.setColorAt(
            0.86,
            QColor(
                48,
                96,
                78,
                255,
            ),
        )

        gradient.setColorAt(
            1.0,
            QColor(
                24,
                45,
                38,
                255,
            ),
        )

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(
            center_x - radius,
            center_y - radius,
            radius * 2,
            radius * 2,
        )

    def _draw_energy(
        self,
        painter,
        center_x,
        center_y,
        radius,
    ):
        orbit_radius = radius * 1.20

        painter.setBrush(Qt.NoBrush)

        purple_pen = QPen(
            QColor(
                174,
                104,
                255,
                190,
            ),
            1.8,
        )

        green_pen = QPen(
            QColor(
                84,
                230,
                158,
                175,
            ),
            1.5,
        )

        painter.setPen(purple_pen)

        start_angle = int(
            (self._phase * 85) % 360
            * 16
        )

        painter.drawArc(
            int(center_x - orbit_radius),
            int(center_y - orbit_radius),
            int(orbit_radius * 2),
            int(orbit_radius * 2),
            start_angle,
            105 * 16,
        )

        painter.setPen(green_pen)

        second_angle = int(
            (-self._phase * 120 + 140) % 360
            * 16
        )

        painter.drawArc(
            int(center_x - orbit_radius * 1.08),
            int(center_y - orbit_radius * 1.08),
            int(orbit_radius * 2.16),
            int(orbit_radius * 2.16),
            second_angle,
            75 * 16,
        )

        energy_x = (
            center_x
            + cos(self._phase * 0.18) * radius * 0.45
        )

        energy_y = (
            center_y
            + sin(self._phase * 0.23) * radius * 0.45
        )

        energy_gradient = QRadialGradient(
            energy_x,
            energy_y,
            radius * 0.55,
        )

        energy_gradient.setColorAt(
            0.0,
            QColor(
                190,
                255,
                225,
                150,
            ),
        )

        energy_gradient.setColorAt(
            0.35,
            QColor(
                75,
                230,
                160,
                70,
            ),
        )

        energy_gradient.setColorAt(
            1.0,
            QColor(
                0,
                0,
                0,
                0,
            ),
        )

        painter.setBrush(energy_gradient)
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(
            energy_x - radius * 0.55,
            energy_y - radius * 0.55,
            radius * 1.10,
            radius * 1.10,
        )
