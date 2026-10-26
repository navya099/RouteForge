# RouteForge

**OPENBVE 루트를 2D/3D에서 직접 그리고, CSV로 추출하는 데스크톱 에디터.**

RouteForge는 OPENBVE 노선 제작 워크플로를 단순화합니다. 평면·종단·횡단 뷰에서 선형을 작성하고, 3D 와이어프레임 뷰에서 오브젝트를 배치한 뒤, CSV로 추출해 OPENBVE에서 결과를 바로 확인할 수 있습니다.

> 코드네임: **Forge** · 패키지: `routeforge` · 진입점: `python -m routeforge`

---

## 주요 기능

- **선형 작성**: LANDXML 선형, XYZ 좌표 선형, 직접 입력 지원
- **다중 뷰**: 평면(Plan) · 종단(Profile) · 횡단(Section) · 3D 와이어프레임
- **오브젝트 배치**: 라이브러리에서 선택 → 뷰에서 클릭 → s/offset 자동 계산
- **CSV 추출**: OPENBVE 호환 오브젝트 CSV 출력
- **REAL VIEW** (예정): 텍스처가 적용된 결과를 별도 창에서 검증

## 로드맵

| 버전 | 코드네임 | 내용 |
|------|----------|------|
| 0.1.0 | Home Signal | MVP: 선형 작성 → 오브젝트 배치 → CSV → OPENBVE 확인 |
| 0.2.0 | Interlocking | 뷰 간 데이터 동기화, 속성 패널 강화 |
| 0.3.0 | Real View | REAL VIEW 창(텍스처 렌더링) 도입 |
| 1.0.0 | First Service | 정식 릴리스 |

## 기술 스택

- **GUI**: PyQt6
- **2D 뷰**: matplotlib (`FigureCanvasQTAgg`)
- **3D 와이어프레임**: pyqtgraph.opengl (`GLViewWidget`)
- **REAL VIEW**: `QOpenGLWidget` (텍스처 바인딩)
- **데이터 모델**: 단일 진실 공급원(SSOT) + Qt 시그널 기반 브로드캐스트

## 설치


git clone https://github.com/<your-org>/routeforge.git
cd routeforge
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .


## 실행

python -m routeforge


## 프로젝트 구조

routeforge/
├── routeforge/
│   ├── core/          # 데이터 모델, 선형 파서, CSV 파서/추출기
│   ├── ui/            # PyQt 메인 윈도우, 팔레트, 뷰 위젯
│   ├── views/         # Plan/Profile/Section/Wireframe3D/RealView
│   └── __main__.py
├── tests/
├── docs/
└── README.md


## 기여 규칙

브랜치: main ← develop ← feature/*, fix/*

커밋: Conventional Commits

스코프: ui, core, csv, parser, view3d, realview

버전: SemVer 2.0 (MAJOR.MINOR.PATCH), 태그는 v0.1.0 형식


## 리이센스


## 5. 라이선스 관련 주의

OPENBVE 자체는 GPL 계열로 배포됩니다. RouteForge는 **OPENBVE의 코드를 링크하지 않고 CSV 파일만 주고받는 별도 프로그램**이므로, MIT 같은 관대한 라이선스를 써도 법적으로 문제는 없습니다. 다만 OPENBVE 오브젝트 파일 포맷을 파싱하는 코드를 OPENBVE 소스에서 직접 가져온다면 GPL 전염이 발생할 수 있으니, **포맷 명세를 문서 기반으로 독립 구현**하는 것을 권장합니다. 초기에는 MIT로 시작하고, 나중에 필요하면 변경하세요.

---
