# routeforge/core/geometry.py
"""선형 위 좌표(s, offset, height) ↔ 월드 좌표 변환기.

BVERouteData.coords/directions를 블록 단위로 보간해 사용한다.
평면·3D·REAL VIEW가 모두 이 모듈을 공유해야 한다.
"""

from __future__ import annotations

import math

from model.bveroutedata import BVERouteData
from routeforge.utils.vector3 import Vector3


def _interp_coord_and_direction(bvedata: BVERouteData, s: float) -> tuple[Vector3, Vector3]:
    """s 위치의 좌표와 진행방향을 블록 보간으로 반환.

    BVERouteData.coords/directions는 block_interval 간격으로 저장되어 있다고 가정.
    범위를 벗어나면 가장 가까운 경계를 사용한다.
    """
    coords = bvedata.coords
    directions = bvedata.directions
    interval = bvedata.block_interval

    if not coords or not directions:
        raise ValueError("bvedata.coords/directions가 비어 있습니다.")
    if interval <= 0:
        raise ValueError("block_interval은 0보다 커야 합니다.")

    # 정규화된 인덱스
    fi = s / interval
    i0 = int(math.floor(fi))
    i1 = i0 + 1
    t = fi - i0

    # 범위 클램프
    if i0 < 0:
        i0 = i1 = 0
        t = 0.0
    elif i1 >= len(coords):
        i0 = i1 = len(coords) - 1
        t = 0.0

    c0, c1 = coords[i0], coords[i1]
    d0, d1 = directions[i0], directions[i1]

    # 좌표 선형 보간
    cx = c0.x + (c1.x - c0.x) * t
    cy = c0.y + (c1.y - c0.y) * t
    cz = c0.z + (c1.z - c0.z) * t

    # 방향 벡터 보간 후 정규화
    dx = d0.x + (d1.x - d0.x) * t
    dy = d0.y + (d1.y - d0.y) * t
    dz = d0.z + (d1.z - d0.z) * t
    norm = math.sqrt(dx * dx + dy * dy + dz * dz) or 1.0
    dx, dy, dz = dx / norm, dy / norm, dz / norm

    return Vector3(cx, cy, cz), Vector3(dx, dy, dz)


def to_plan_xy(bvedata: BVERouteData, s: float, offset: float) -> tuple[float, float]:
    """(s, offset) → 평면 좌표 (x, y).

    offset은 진행방향의 오른쪽(법선)으로 적용한다.
    좌표계는 2D 평면(X, Y)이며, 진행방향을 XY 평면에 투영해 법선을 구한다.
    """
    coord, direction = _interp_coord_and_direction(bvedata, s)

    # 진행방향의 XY 평면 투영
    dx, dy = direction.x, direction.y
    norm2d = math.hypot(dx, dy) or 1.0
    dx, dy = dx / norm2d, dy / norm2d

    # 오른쪽 법선: (dx, dy)를 -90도 회전 → (dy, -dx)
    nx, ny = dy, -dx

    x = coord.x + nx * offset
    y = coord.y + ny * offset
    return x, y


def to_world_xyz(
    bvedata: BVERouteData,
    s: float,
    offset: float,
    height: float,
) -> tuple[float, float, float]:
    """(s, offset, height) → 3D 월드 좌표 (x, y, z).

    height는 월드 Z축(수직)으로 적용한다.
    """
    coord, direction = _interp_coord_and_direction(bvedata, s)

    # XY 평면 법선 (to_plan_xy와 동일 로직)
    dx, dy = direction.x, direction.y
    norm2d = math.hypot(dx, dy) or 1.0
    dx, dy = dx / norm2d, dy / norm2d
    nx, ny = dy, -dx

    x = coord.x + nx * offset
    y = coord.y + ny * offset
    z = coord.z + height
    return x, y, z