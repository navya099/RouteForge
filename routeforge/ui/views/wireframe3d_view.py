"""3D 와이어프레임 뷰: 선로 중심선과 오브젝트 점을 표시."""

from __future__ import annotations

import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph import Vector
from PyQt6.QtWidgets import QVBoxLayout

from routeforge.ui.views.base_view import BaseView
from routeforge.core.model.model import RouteData

class Wireframe3DView(BaseView):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._data: RouteData | None = None
        self._camera_initialized = False

        # 3D 뷰포트 생성
        self.view = gl.GLViewWidget()
        self.view.setBackgroundColor((30, 30, 30, 255)) # 어두운 배경

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        # 바닥 기준 격자
        self.grid = gl.GLGridItem()
        self.grid.setSize(x=50000, y=50000) # 선로 스케일에 맞춰 크게 설정
        self.grid.setSpacing(x=1000, y=1000)
        self.view.addItem(self.grid)

    def set_data(self, data: RouteData) -> None:
        self._data = data
        self._camera_initialized = False # 새 데이터 로드 시 카메라 초기화 허용
        self.redraw()

    def redraw(self) -> None:
        # 기존 아이템 제거 (그리드는 유지)
        for item in self.view.items[:]:
            if item is not self.grid:
                self.view.removeItem(item)

        if self._data is None or not self._data.has_bvedata:
            return

        bvedata = self._data.bvedata

        # 1) 선로 중심선 (bvedata.coords)
        track_points = np.array([[c.x, c.y, c.z] for c in bvedata.coords])
        if len(track_points) > 0:
            track_line = gl.GLLinePlotItem(
                pos=track_points,
                color=(0.3, 0.6, 1.0, 1.0), # 파란색
                width=2,
                antialias=True
            )
            self.view.addItem(track_line)

        # 2) 오브젝트 점 (data.objects)
        if self._data.has_objects:
            from routeforge.core.geometry import to_world_xyz
            obj_points = []
            skipped = 0
            for obj in self._data.objects:
                try:
                    x, y, z = to_world_xyz(bvedata, obj.track_position, obj.offset, obj.height)
                    obj_points.append([x, y, z])
                except Exception as e:
                    skipped += 1
                    if skipped <= 3:  # 처음 3개만 에러 출력
                        print(f"DEBUG ERROR: {e}")
                    continue

            print(f"DEBUG: 전체 오브젝트 {len(self._data.objects)}개 중 변환 성공 {len(obj_points)}개, 실패 {skipped}개")
            if obj_points:
                print(f"DEBUG: 첫 오브젝트 좌표 = {obj_points[0]}")
                obj_arr = np.array(obj_points)
                scatter = gl.GLScatterPlotItem(
                    pos=obj_arr,
                    color=(1.0, 1.0, 0.3, 1.0), # 노란색
                    size=5.0,
                    pxMode=True
                )
                self.view.addItem(scatter)

        # 3) 최초 1회 카메라 중심을 선로 중앙으로 이동
        if not self._camera_initialized and len(track_points) > 0:
            center = track_points.mean(axis=0)
            min_pt = track_points.min(axis=0)
            max_pt = track_points.max(axis=0)
            size = max_pt - min_pt

            max_dim = float(max(size[0], size[1], size[2]))
            distance = max_dim * 1.5 if max_dim > 0 else 1000.0

            # pyqtgraph 내부 호환성을 위해 Vector 객체 사용
            self.view.opts['center'] = Vector(
                float(center[0]), float(center[1]), float(center[2])
            )
            self.view.opts['distance'] = distance
            self.view.opts['elevation'] = 15
            self.view.opts['azimuth'] = 45

            self.view.update() # 변경된 카메라 옵션 즉시 적용
            self._camera_initialized = True