"""모든 뷰가 구현해야 하는 공통 인터페이스."""

from __future__ import annotations

from abc import abstractmethod

from PyQt6.QtWidgets import QWidget

from routeforge.core.model import RouteData


class BaseView(QWidget):
    """모든 편집 뷰의 추상 베이스.

    QStackedWidget에 넣어 뷰 전환을 통일하기 위한 최소 계약만 정의한다.
    """

    @abstractmethod
    def set_data(self, data: RouteData) -> None:
        """데이터 모델을 주입한다."""

    @abstractmethod
    def redraw(self) -> None:
        """현재 데이터 기준으로 다시 그린다."""