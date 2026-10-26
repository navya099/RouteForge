"""RouteForge 단일 진실 공급원(SSOT)."""

from __future__ import annotations

from dataclasses import dataclass, field

from routeforge.Profile.profile import Profile
from routeforge.core.model.bveroutedata import BVERouteData
from routeforge.core.model.ipdata import BasePoint


@dataclass
class RouteData:
    """모든 뷰가 공유하는 루트 데이터(파사드).

    초기 마이그레이션 단계에서는 기존 도메인 객체(BasePoint 하위,
    BVERouteData, Profile)를 그대로 보관한다. 이후 내부 표현을 교체하되,
    뷰는 이 인터페이스에만 의존한다.
    """

    alignments: list[BasePoint] = field(default_factory=list)
    bvedata: BVERouteData | None = None
    profile: Profile | None = None

    # --- 편의 접근자 ---
    @property
    def has_alignment(self) -> bool:
        return bool(self.alignments)

    @property
    def has_bvedata(self) -> bool:
        return self.bvedata is not None and bool(self.bvedata.coords)

    @property
    def has_profile(self) -> bool:
        return self.profile is not None and len(self.profile.pvis) > 0