
from tkinter import messagebox

from routeforge.core.model.model import PlacedObject


class CSVRouteParser:
    """
       BVEParser를 래핑하는 클래스.

       Attributes:
           current_route (CurrentRoute): openbve CurrentRoute객체
       """
    def __init__(self):
        self.current_route = None
        self.route_data = None
    def parse_route(self, filename: str):
        """
        BVEParser를 래핑하여 파싱하는 메소드
        Attributes:
            filename(str): 루트 전체경로
        """

        #BVE 객체 초기화
        from routeforge.RouteLoader import RouteLoader
        loader = RouteLoader(filename)
        result = loader.load()
        self.current_route = loader.current_route
        # 파서가 CurrentRoute.route_data에 RouteData를 보관함
        self.route_data = getattr(loader.current_route, "route_data", None)
        messagebox.showinfo("실행 결과", f'파싱 {result[0]}')


    def extract_currentroute(self):
        """
        CurrentRoute를 파싱하여 데이터를 추출하는 메소드
        Returns:
        list: 다음 5개 리스트로 구성된 리스트
            - trackpositions (list[float]): 측점
            - radiuss (list[float]): 곡선 반경 (m 단위, 직선은 0)
            - pitchs (list[float]): 종단 구배 값 (0.001)
            - stations (list[float, str]): 정거장 정보(측점, 이름)
            - coords (list[Vector3]): 좌표
            - directions (list[Vector3]): 3d방향각
        """
        trackpositions, radiuss, pitchs, coords, directions = [], [], [], [], []
        stations = []

        # 트랙 요소 (리스트 순회)
        for elem in self.current_route.Tracks[0].Elements:
            trackpositions.append(elem.StartingTrackPosition)
            radiuss.append(elem.CurveRadius)
            pitchs.append(elem.Pitch)
            coords.append(elem.WorldPosition)
            directions.append(elem.WorldDirection)

        # 정거장 요소
        for station in self.current_route.Stations:
            name = station.Name
            position = station.DefaultTrackPosition
            stations.append([position, name])

        #초기표고
        firstelevation = self.current_route.Atmosphere.InitialElevation
        return [trackpositions, radiuss, pitchs, stations, coords, directions, firstelevation]

    def extract_objects(self) -> list:
        """RouteData.Blocks에서 FreeObj를 추출해 PlacedObject 리스트로 반환."""

        if self.route_data is None or not hasattr(self.route_data, "Blocks"):
            return []

        objects: list[PlacedObject] = []

        for block in self.route_data.Blocks:
            # 1. RailFreeObj: Dict[int, List[FreeObj]]
            for rail_index, free_objs in block.RailFreeObj.items():
                for fo in free_objs:
                    objects.append(self._to_placed_object(fo))

            # 2. GroundFreeObj: List[FreeObj]
            for fo in block.GroundFreeObj:
                objects.append(self._to_placed_object(fo))

        return objects

    @staticmethod
    def _to_placed_object(fo) -> PlacedObject:
        return PlacedObject(
            track_position=float(fo.TrackPosition),
            type_index=int(fo.Type),
            object_path="",  # 경로 해석은 나중에 (ObjectDictionary 필요)
            offset=float(fo.Position.x),
            height=float(fo.Position.y),
            yaw=float(fo.Yaw),
            pitch=float(fo.Pitch),
            roll=float(fo.Roll),
        )