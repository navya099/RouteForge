"""RouteForge 단일 진실 공급원(SSOT)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class RouteData:
    """모든 뷰가 공유하는 루트 데이터.

    기존 BVERouteData/Profile/alignments를 이 모델로 흡수하거나,
    임시로 이 안에 참조를 담아 두고 단계적으로 마이그레이션한다.
    """

    alignments: list[Any] = field(default_factory=list)
    bvedata: Any | None = None
    profile: Any | None = None