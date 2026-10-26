"""평면 뷰: IP 라인, 곡선(FL), IP 제원을 matplotlib으로 표시."""

from __future__ import annotations

import matplotlib

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
)
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QVBoxLayout

from routeforge.core.model.ipdata import IPdata
from routeforge.core.model.model import RouteData
from routeforge.ui.views.base_view import BaseView

# 한글 폰트 (전역). PyQt 앱 시작 전에 한 번만 설정해도 되지만,
# 뷰 단위로 두면 다른 뷰에서도 동일하게 적용된다.
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False


class PlanView(BaseView):
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

        # 초기: 빈 도화지
        self.ax.grid(True)
        self.ax.axis("off")
        self.canvas.draw()

    # --- BaseView 구현 ---
    def set_data(self, data: RouteData) -> None:
        self._data = data
        self.redraw()

    def redraw(self) -> None:
        self.ax.clear()

        if self._data is None or not self._data.has_alignment:
            self.ax.axis("off")
            self.canvas.draw()
            return

        self._apply_decoration("평면", "X(N)", "Y(E)")

        alignments = self._data.alignments

        # 1) IP 라인
        x_ip = [a.coord.x for a in alignments]
        y_ip = [a.coord.y for a in alignments]
        if x_ip and y_ip:
            self.ax.plot(x_ip, y_ip, color="gray", label="IP라인")
            self._set_fixed_view(x_ip, y_ip)

        # 2) IP 제원

        n = len(alignments)
        for i, a in enumerate(alignments):
            if i == 0:
                text = "BP"
            elif i == n - 1:
                text = "EP"
            elif isinstance(a, IPdata):
                radius_text = self._format_radius(a.radius)
                text = f"IP{a.ipno}\nR={radius_text}"
            else:
                # EndPoint가 중간에 있는 비정상 케이스 — 방어적 표시
                text = f"BP/EP?"
            self.ax.text(a.coord.x, a.coord.y, text)

        # 3) 곡선(FL)
        if self._data.has_bvedata:
            x_fl = [c.x for c in self._data.bvedata.coords]
            y_fl = [c.y for c in self._data.bvedata.coords]
            if x_fl and y_fl:
                self.ax.plot(x_fl, y_fl, color="red", label="FL")

        # 4) 오브젝트
        if self._data.has_objects and self._data.has_bvedata:
            from routeforge.core.geometry import to_plan_xy
            ox, oy = [], []
            for obj in self._data.objects:
                try:
                    x, y = to_plan_xy(self._data.bvedata, obj.track_position, obj.offset)
                    ox.append(x)
                    oy.append(y)
                except Exception:
                    continue
            if ox and oy:
                self.ax.scatter(ox, oy, color="blue", s=10, label=f"오브젝트({len(ox)})", zorder=5)
        self.ax.legend()
        self.canvas.draw()

    @staticmethod
    def _format_radius(radius: float | tuple[float, ...]) -> str:
        if isinstance(radius, tuple):
            return ", ".join(f"{r:g}" for r in radius)
        return f"{radius:g}"

    # --- 기존 plot.py 헬퍼 이식 ---
    def _apply_decoration(
        self,
        title: str,
        xlabel: str,
        ylabel: str,
        show_grid: bool = True,
        set_aspect: str = "equal",
    ) -> None:
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        if show_grid:
            self.ax.grid(True)
        self.ax.axis("on")
        self.ax.set_aspect(set_aspect)

    def _set_fixed_view(
        self, x_data: list[float], y_data: list[float], box_size: float = 1000
    ) -> None:
        if not x_data or not y_data:
            return

        x_center = (max(x_data) + min(x_data)) / 2
        y_center = (max(y_data) + min(y_data)) / 2

        data_width = max(x_data) - min(x_data)
        data_height = max(y_data) - min(y_data)

        half_box = box_size / 2
        scale_x = data_width / box_size if data_width > box_size else 1
        scale_y = data_height / box_size if data_height > box_size else 1
        scale = max(scale_x, scale_y)

        half_width = half_box * scale
        half_height = half_box * scale

        self.ax.set_xlim(x_center - half_width, x_center + half_width)
        self.ax.set_ylim(y_center - half_height, y_center + half_height)
        self.ax.set_aspect("equal")