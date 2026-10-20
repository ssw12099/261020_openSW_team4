# 오픈소스SW 팀 프로젝트 — Streamlit 모듈형 기본 틀

교수님 강의자료 33~35페이지의 G1~G7 기능 구성을 토대로 만든 **팀 협업용 시작 프로젝트**입니다.
현재 게임 동작은 구현되지 않았고, **각 게임을 나중에 독립적으로 추가할 수 있는 실행 틀만** 있습니다.

## 1. 설치와 실행 (Windows / VS Code)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

개발 환경에서 PowerShell 실행 정책에 의해 활성화가 차단되면 `cmd` 터미널에서
`.venv\Scripts\activate.bat`를 사용해도 됩니다.

## 2. 폴더 구조

```text
app.py                 # 메인 화면, 게임 메뉴 및 모듈 라우팅 (팀장 관리)
core/state.py          # 공통 완료/재시작/초기화 상태 관리 (팀장 관리)
games/g1.py            # G1 게임 A+B
games/g2.py            # G2 게임 A+B
games/g3.py            # G3 게임 A+B
games/g4.py            # G4 게임 A+B
games/g5.py            # G5 게임 A+B
games/g6.py            # G6 게임 A+B
games/g7.py            # G7 게임 A+B
requirements.txt       # 필요한 Python 패키지
.gitignore             # 로컬 개발 파일 제외
README.md              # 팀 공동 작업 규칙
```

## 3. 팀원 공통 규칙 — 반드시 지키기

1. **담당 파일만 수정:** 예: G3 담당자는 `games/g3.py`에서 작업합니다. 다른 사람의 게임 파일이나 `app.py`, `core/state.py`는 임의로 수정하지 않습니다.
2. **엔트리 함수:** 각 `games/gN.py`에서 `def render() -> None:` 함수를 반드시 유지합니다.
3. **완료 처리:** 실제 게임 완료 조건을 만족한 후 `complete_game("G3")`처럼 자신의 게임 ID만 전달합니다.
4. **위젯 상태 키:** 팀 간 충돌 방지를 위해 `key="g3_answer"`처럼 **게임 번호 소문자 + 언더스코어** 접두사를 사용합니다. 직접 `st.session_state`에 값을 넣는 경우에도 동일합니다.
5. **재시작:** 자기 게임만 다시 할 때는 `reset_game("G3")`을 사용합니다. 전체 리셋은 G7 구현에서 `reset_all_games()`을 호출합니다.
6. **가져오기:** 자기 게임에서 공통 함수를 호출하려면 `from core.state import complete_game, reset_game`을 사용합니다.
7. **요구사항 유지:** 교수님 PDF 33페이지의 A/B 기능을 한 게임 파일에서 함께 구현합니다.
8. **추가 라이브러리:** 새 라이브러리가 필요하면 PR 설명에 기록하고 `requirements.txt` 변경을 팀장과 사전에 조율합니다.

**예시:**

```python
# games/g3.py
import streamlit as st
from core.state import complete_game, is_complete, reset_game

def render() -> None:
    st.subheader("G3. 수상한 강의 공지")
    # TODO: G3-A/G3-B 실제 게임 구현
    # 모든 조건을 만족했을 때만 complete_game("G3")
    if is_complete("G3"):
        st.success("G3 완료")
```

## 4. 브랜치와 PR

- `main`: 최종 제출용
- `dev`: 완성된 기능을 모아 통합 테스트
- `feature/G1` ~ `feature/G7`: 게임별 브랜치. 각 게임의 A/B 기능은 **하나의 브랜치**에서 구현
- PR 대상 브랜치: `dev`

예: G1 기능 구현 시작

```powershell
git switch dev
git pull origin dev
git switch -c feature/G1
# games/g1.py 에서 기능 구현
git add games/g1.py
git commit -m "feat: implement G1 game"
git push -u origin feature/G1
```

GitHub에서 **base: dev ← compare: feature/G1** Pull Request를 생성하고
코드 확인 후 머지하세요. G2의 브랜치는 최신 dev에서 새로 시작합니다.

## 5. 상태 관리 API

| 함수 | 목적 |
|---|---|
| `initialize_state()` | 완료 상태 초기화 (앱이 자동 호출) |
| `is_complete("G1")` | G1 완료 여부 확인 |
| `complete_game("G1")` | 게임 완료 기록 |
| `reset_game("G1")` | 해당 게임만 재시작 |
| `completed_count()` | 완료 게임 수 |
| `all_prerequisites_complete()` | G1~G6를 모두 완료했는지 확인 |
| `reset_all_games()` | G1~G7 모두 초기화 |

Streamlit의 `st.session_state`는 사용자의 **현재 브라우저 세션**을 기준으로 동작합니다.
서버에 영구 저장되는 데이터베이스가 아니므로, 재접속/세션 종료 후에는 진행 상황이 유지되지 않을 수 있습니다.

## 6. 통합 시 팀장 점검

- `python -m streamlit run app.py`가 오류 없이 실행되는가?
- 게임 메뉴의 G1~G7 각각 진입할 수 있는가?
- 각 게임 완료 후 왼쪽 메뉴의 완료 표시가 바뀌는가?
- 다른 게임으로 이동해도 현재 세션의 완료 상태가 유지되는가?
- 게임 재시작/전체 초기화가 의도대로 되는가?
- 서로 다른 게임의 위젯 `key`가 충돌하지 않는가?
