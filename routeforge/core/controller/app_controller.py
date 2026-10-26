# 기능 클래스(모든 기능을 넣을 예정)
from routeforge.core.datacontainer import BVERouteFactory
from routeforge.core.parser import CSVRouteParser


class AppController:
    """
    기능 관리 클래스.

    Attributes:
        current_route (CurrentRoute): openbve CurrentRoute객체 노선의 트랙, 곡선, 구배, 좌표, 역 정보를 포함.
        main_app (tk.Tk) TK 메인 인스턴스
        file_ctrl(FileController): 파일 열기/저장 및 경로 관리를 담당하는 컨트롤러
        parser (CSVRouteParser): CSVRouteParser 호출용 클래스
    """
    def __init__(self, main_app, file_controller):
        self.current_route = None
        self.main_app = main_app  # MainApp 인스턴스 (UI 접근용)
        self.file_ctrl = file_controller
        # Alignment 데이터 컨테이너
        self.alignments = None
        self.bvedata = None
        self.profile = None

        # 기능 전담 클래스 인스턴스 보관
        self.parser = CSVRouteParser()

    def load_route(self, filepath: str):
        """
        파일에서 BVE 루트를 로드하고, 필요한 데이터 리스트를 반환.
        Attributes:
            filepath (str): 루트파일 경로
        Returns:
            list: 다음 6개 리스트로 구성된 리스트
            - trackpositions (list[float]): 궤도 상의 절대 거리 (m 단위)
            - radiuss (list[float]): 곡선 반경 (m 단위, 직선은 0)
            - pitch_values (list[float]): 종단 구배 값 (%)
            - station_names (list[str]): 역 이름
            - coords (list[Vector3]): 각 지점의 좌표 (X, Y, Z)
            - directions (list[Vector3]): 각 지점에서의 진행 방향 벡터
        """
        self.parser.parse_route(filepath) #루트 파싱 실행
        self.current_route = self.parser.current_route # 파싱후 current_route 저장
        datalist = self.parser.extract_currentroute() # 필요한 요소만 리스트로 추출
        return datalist

    def convert_to_bveroute(self, extracted_currentroute_list: list):
        """
        extract_currentroute에서 반환된 리스트를 BVERouteData 객체로 변환.

        Args:
            extracted_currentroute_list (list): extract_currentroute에서 반환된 6개 리스트

        Returns:
            BVERouteData: 변환된 BVERouteData 객체
        """
        self.bvedata = BVERouteFactory.from_current_route(extracted_currentroute_list)