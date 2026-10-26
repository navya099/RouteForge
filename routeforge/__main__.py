"""RouteForge 진입점: python -m routeforge"""

from __future__ import annotations

import sys


def main() -> int:
    from routeforge.ui.main_window import MainWindow
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setApplicationName("RouteForge")
    app.setApplicationVersion(__import__("routeforge").__version__)

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())