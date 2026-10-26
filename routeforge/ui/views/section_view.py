"""횡단 뷰: 현재 측점에서의 FL 표고점 표시.

MVP 단계에서는 선로 중심선(offset=0) 위의 FL 표고점 하나만 표시한다.
오브젝트 단계에서 (offset, height) 점들을 같은 뷰에 추가할 예정.
"""

from __future__ import annotations

import matplotlib
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
)
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QVBoxLayout


from routeforge.ui.views.base_view import BaseView
from routeforge.core.model.model import RouteData
from routeforge.utils.utils import format_distance

matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False


class SectionView(BaseView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)


        self._data: RouteData | None = None
        self._station: float | None = None  # 현재 측점 s

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

        # MVP: 측점이 지정되지 않았으면 bvedata 중앙을 기본값으로
        if self._station is None and data.has_bvedata:
            self._station = 120

        self.redraw()

    # --- 외부에서 측점 변경용 (향후 평면 클릭/슬라이더에서 호출) ---
    def set_station(self, station: float) -> None:
        self._station = station
        self.redraw()

    def redraw(self) -> None:
        self.ax.clear()

        if (
            self._data is None
            or not self._data.has_profile
            or self._station is None
        ):
            self.ax.axis("off")
            self.canvas.draw()
            return

        # --- 데코레이션 ---
        self.ax.set_title(f"횡단 (s = {format_distance(self._station)} m)")
        self.ax.set_xlabel("Offset (m)")
        self.ax.set_ylabel("Height (m)")
        self.ax.grid(True)
        self.ax.axis("on")
        self.ax.set_aspect("equal")

        # --- FL 표고점 ---
        elevation = self._data.profile.elevation_at_station(self._station)

        # 선로 중심선(offset=0) 위 표고점
        self.ax.plot(0.0, elevation, marker="o", color="red", label="FL 표고점")
        self.ax.text(
            0.0, elevation,
            f"  s={self._station:.1f}\n  EL={elevation:.3f}",
            va="bottom", ha="left", fontsize=9,
        )
        # --- 현재 측점 근처 오브젝트 ---
        if self._data.has_objects:
            tolerance = 1.0  # ±1m 이내 오브젝트만 (MVP)
            nearby = [
                obj for obj in self._data.objects
                if abs(obj.track_position - self._station) <= tolerance
            ]
            if nearby:
                ox = [obj.offset for obj in nearby]
                oy = [elevation + obj.height for obj in nearby]
                self.ax.scatter(ox, oy, color="blue", s=30, label=f"오브젝트({len(nearby)})", zorder=6)

        # --- 표시 범위: 점 주변 고정 윈도우 ---
        # MVP: 단일 점이라 주변 여백을 고정 크기로 잡는다.
        half_w = 5.0  # offset ±5m
        half_h = 5.0  # height ±5m
        self.ax.set_xlim(-half_w, +half_w)
        self.ax.set_ylim(elevation - half_h, elevation + half_h)

        self.ax.legend(loc="upper right")
        self.canvas.draw()