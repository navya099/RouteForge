# 버전 관리 규칙

## 버전 번호 (SemVer 2.0)

- **MAJOR**: CSV 출력 포맷 또는 프로젝트 파일 스키마가 호환 불가하게 변경
- **MINOR**: 기능 추가 (하위 호환 유지)
- **PATCH**: 버그 수정, 성능 개선, UI 문구 변경

MVP 개발 중에는 `0.x.y`. MVP 완료 시 `0.1.0` 태깅.

## 코드네임

| 버전 | 코드네임 | 내용 |
|------|----------|------|
| 0.1.0 | Home Signal | MVP |
| 0.2.0 | Interlocking | 뷰 동기화 |
| 0.3.0 | Real View | REAL VIEW 창 |
| 1.0.0 | First Service | 정식 릴리스 |

## Git 태그

`v0.1.0` 형식.

## 커밋 (Conventional Commits)

스코프: `ui`, `core`, `csv`, `parser`, `view3d`, `realview`