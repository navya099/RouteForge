"""RouteForge 메인 윈도우: 메뉴 + 툴바 + Dock + QStackedWidget + 상태바."""

from __future__ import annotations

from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QDockWidget,
    QLabel,
    QListWidget,
    QMainWindow,
    QStackedWidget,
    QWidget,
)


class PlaceholderView(QWidget):
    """이식 전 임시 뷰. 실제 뷰로 교체 예정."""

    def __init__(self, name: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._name = name

    def set_data(self, data) -> None:  # noqa: ANN001
        pass

    def redraw(self) -> None:
        pass


class MainWindow(QMainWindow):
    VIEW_PLAN = 0
    VIEW_PROFILE = 1
    VIEW_SECTION = 2
    VIEW_3D = 3

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("RouteForge")
        self.resize(1200, 800)

        self._build_central()
        self._build_docks()
        self._build_menu()
        self._build_statusbar()

    # --- 중앙: QStackedWidget ---
    def _build_central(self) -> None:
        self.stack = QStackedWidget()
        self.views = {
            self.VIEW_PLAN: PlaceholderView("Plan"),
            self.VIEW_PROFILE: PlaceholderView("Profile"),
            self.VIEW_SECTION: PlaceholderView("Section"),
            self.VIEW_3D: PlaceholderView("Wireframe3D"),
        }
        for view in self.views.values():
            self.stack.addWidget(view)
        self.setCentralWidget(self.stack)

    # --- 좌/우 Dock ---
    def _build_docks(self) -> None:
        # 좌: 오브젝트 라이브러리
        self.library_dock = QDockWidget("오브젝트 라이브러리", self)
        self.library_dock.setWidget(QListWidget())
        self.addDockWidget(self._left_area(), self.library_dock)

        # 우: 속성
        self.properties_dock = QDockWidget("속성", self)
        self.properties_dock.setWidget(QLabel("선택된 항목 없음"))
        self.addDockWidget(self._right_area(), self.properties_dock)

    # --- 메뉴/툴바 ---
    def _build_menu(self) -> None:
        view_menu = self.menuBar().addMenu("보기")

        actions = [
            ("평면 뷰", "F6", self.VIEW_PLAN),
            ("종단 뷰", "F7", self.VIEW_PROFILE),
            ("횡단 뷰", "F8", self.VIEW_SECTION),
            ("3D 와이어프레임 뷰", "F9", self.VIEW_3D),
        ]
        for label, shortcut, index in actions:
            act = QAction(label, self)
            act.setShortcut(QKeySequence(shortcut))
            act.triggered.connect(lambda _=False, i=index: self.stack.setCurrentIndex(i))
            view_menu.addAction(act)

        view_menu.addSeparator()
        real_view_act = QAction("REAL VIEW 열기...", self)
        real_view_act.setShortcut(QKeySequence("Ctrl+R"))
        real_view_act.triggered.connect(self._open_real_view)
        view_menu.addAction(real_view_act)

    def _open_real_view(self) -> None:
        # TODO: RealViewWindow 구현 후 연결
        pass

    # --- 상태바 ---
    def _build_statusbar(self) -> None:
        self.status_coord = QLabel("좌표: -")
        self.status_s = QLabel("s: -")
        self.status_selection = QLabel("선택: 없음")
        bar = self.statusBar()
        bar.addWidget(self.status_coord)
        bar.addWidget(self.status_s)
        bar.addPermanentWidget(self.status_selection)

    # --- 유틸 ---
    def _left_area(self):
        from PyQt6.QtCore import Qt
        return Qt.DockWidgetArea.LeftDockWidgetArea

    def _right_area(self):
        from PyQt6.QtCore import Qt
        return Qt.DockWidgetArea.RightDockWidgetArea