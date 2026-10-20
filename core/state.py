"""게임 간에 공유하는 완료 상태 관리 (Streamlit 세션 단위)."""
import streamlit as st

GAME_IDS = tuple(f"G{i}" for i in range(1, 8))
_COMPLETED_KEY = "completed_games"


def _check_game_id(game_id: str) -> None:
    if game_id not in GAME_IDS:
        raise ValueError(f"지원하지 않는 게임 ID: {game_id}")


def initialize_state() -> None:
    """처음 접속하면 G1~G7의 완료 상태를 False로 만듭니다."""
    if _COMPLETED_KEY not in st.session_state:
        st.session_state[_COMPLETED_KEY] = {game_id: False for game_id in GAME_IDS}


def is_complete(game_id: str) -> bool:
    _check_game_id(game_id)
    initialize_state()
    return bool(st.session_state[_COMPLETED_KEY][game_id])


def complete_game(game_id: str) -> None:
    """실제 완료 조건을 충족한 경우에만 호출합니다."""
    _check_game_id(game_id)
    initialize_state()
    progress = st.session_state[_COMPLETED_KEY].copy()
    progress[game_id] = True
    st.session_state[_COMPLETED_KEY] = progress


def completed_count() -> int:
    initialize_state()
    return sum(bool(done) for done in st.session_state[_COMPLETED_KEY].values())


def all_prerequisites_complete() -> bool:
    """G7의 시작 조건: G1~G6를 모두 완료했는지 확인합니다."""
    return all(is_complete(game_id) for game_id in GAME_IDS[:6])


def reset_game(game_id: str) -> None:
    """한 게임만 처음부터 다시 시작합니다. 해당 게임의 위젯 상태도 삭제합니다."""
    _check_game_id(game_id)
    initialize_state()
    progress = st.session_state[_COMPLETED_KEY].copy()
    progress[game_id] = False
    st.session_state[_COMPLETED_KEY] = progress
    prefix = game_id.lower() + "_"
    for key in list(st.session_state):
        if key.startswith(prefix):
            del st.session_state[key]


def reset_all_games() -> None:
    """G7의 전체 초기화 버튼 등에서 사용합니다."""
    for key in list(st.session_state):
        if key == _COMPLETED_KEY or any(
            key.startswith(game_id.lower() + "_") for game_id in GAME_IDS
        ):
            del st.session_state[key]
    initialize_state()
