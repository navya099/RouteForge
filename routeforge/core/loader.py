# routeforge/core/loader.py
"""파일 → RouteData 로더. GUI와 무관한 파서 조합 로직."""

from __future__ import annotations

from pathlib import Path

from routeforge.core.alignment.alginmentcalculator import AlignmentCalculator
from routeforge.core.alignment.alignmentbuilder import AlignmentBuilder
from routeforge.core.controller.app_controller import AppController
from routeforge.core.controller.file_controller import FileController
from routeforge.core.model.model import RouteData
from routeforge.core.processor import RouteProcessor
from routeforge.core.profile.profilebuilder import ProfileBuilder


class RouteLoader:
    """EventHandler._process_and_plot의 파서 조합을 재사용하되,
    GUI(tkinter/Qt)에 의존하지 않도록 AppController를 main_app=None으로 생성.
    """

    def __init__(self) -> None:
        # FileController는 filepath 속성만 쓰므로 GUI 무관
        self._file = FileController()
        # AppController의 파서 경로는 main_app을 쓰지 않으므로 None 허용
        self._app = AppController(None, self._file)

    def set_filepath(self, path: str) -> None:
        """PyQt QFileDialog 결과를 FileController에 주입."""
        self._file.filepath = path

    def load(self, filepath: str | Path) -> RouteData | None:
        self._file.filepath = str(filepath)

        extracted_list = self._app.load_route(str(filepath))
        if not extracted_list:
            return None

        self._app.convert_to_bveroute(extracted_list)
        bve_data = self._app.bvedata

        RouteProcessor(bve_data).run()
        alignments = AlignmentBuilder.build_ipdata_from_sections(bve_data)
        AlignmentCalculator().calculate_stationinfo(bve_data)
        profile = ProfileBuilder.build_profile(bve_data)

        self._app.profile = profile
        self._app.alignments = alignments

        return RouteData(
            alignments=alignments,
            bvedata=bve_data,
            profile=profile,
        )