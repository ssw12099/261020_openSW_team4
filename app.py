"""팀 공통 Streamlit 진입점. 각 게임 코드는 games/ 아래에 작성합니다."""
import streamlit as st

from core.state import GAME_IDS, completed_count, initialize_state, is_complete
from games import g1, g2, g3, g4, g5, g6, g7

GAME_NAMES = {
    "G1": "까다로운 출첵봇",
    "G2": "청개구리 퀴즈",
    "G3": "수상한 강의 공지",
    "G4": "팀플 빌런과 협상",
    "G5": "고장난 계산기",
    "G6": "기말 범위 기억하기",
    "G7": "종강 버튼의 배신",
}

# 팀원은 games/gN.py 파일의 render()만 구현합니다.
GAME_RENDERERS = {
    "G1": g1.render,
    "G2": g2.render,
    "G3": g3.render,
    "G4": g4.render,
    "G5": g5.render,
    "G6": g6.render,
    "G7": g7.render,
}


def main():
    st.set_page_config(page_title="오픈소스SW 팀 게임", page_icon="🎮", layout="wide")
    initialize_state()

    with st.sidebar:
        st.title("🎮 팀 프로젝트")
        game_id = st.radio(
            "플레이할 게임",
            options=GAME_IDS,
            format_func=lambda value: (
                f"{'✅' if is_complete(value) else '⬜'} {value}. {GAME_NAMES[value]}"
            ),
            key="selected_game",
        )
        st.divider()
        st.progress(completed_count() / len(GAME_IDS))
        st.caption(f"완료: {completed_count()} / {len(GAME_IDS)}")

    st.title("오픈소스SW 팀 프로젝트")
    # G1~G7 각각 render()를 내보내므로 app.py 수정 없이 모듈만 교체할 수 있습니다.
    GAME_RENDERERS[game_id]()


if __name__ == "__main__":
    main()
