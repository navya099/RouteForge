"""종단 뷰: PVI 라인(FL)을 matplotlib으로 표시."""

from __future__ import annotations

import matplotlib
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
)
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QVBoxLayout

from routeforge.core.model.model import RouteData
from routeforge.ui.views.base_view import BaseView

matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False


class ProfileView(BaseView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._data: RouteData | None = None

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas, stretch=1)
        layout.addWidget(self.toolbar)

        self.ax.axis("off")
        self.canvas.draw()

    # --- BaseView 구현 ---
    def set_data(self, data: RouteData) -> None:
        self._data = data
        self.redraw()

    def redraw(self) -> None:
        self.ax.clear()

        if self._data is None or not self._data.has_profile:
            self.ax.axis("off")
            self.canvas.draw()
            return

        self._apply_decoration("종단", "X(거리)", "Y(표고)")

        pvis = self._data.profile.pvis
        x_data = [p.station for p in pvis]
        y_data = [p.elevation for p in pvis]

        if x_data and y_data:
            self.ax.plot(x_data, y_data, color="red", label="FL")

            # 종단은 등축척이 아니라 auto. 여백만 조금 둔다.
            x_min, x_max = min(x_data), max(x_data)
            y_min, y_max = min(y_data), max(y_data)
            x_pad = (x_max - x_min) * 0.02 if x_max > x_min else 1.0
            y_pad = (y_max - y_min) * 0.10 if y_max > y_min else 1.0
            self.ax.set_xlim(x_min - x_pad, x_max + x_pad)
            self.ax.set_ylim(y_min - y_pad, y_max + y_pad)

        self.ax.legend()
        self.canvas.draw()

    def _apply_decoration(
        self,
        title: str,
        xlabel: str,
        ylabel: str,
        show_grid: bool = True,
    ) -> None:
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        if show_grid:
            self.ax.grid(True)
        self.ax.axis("on")
        self.ax.set_aspect("auto")