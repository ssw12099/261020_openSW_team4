"""G7: 종강 버튼의 배신 — G1~G6 선행 완료 및 암호 확인, 전체 초기화."""

import streamlit as st

from core.state import (
    GAME_IDS,
    all_prerequisites_complete,
    complete_game,
    is_complete,
    reset_all_games,
    reset_game,
)

G7_PASSWORD = "별빛"  # G5 단서 '별' + G6 단서 '빛'


def initialize_g7_state() -> None:
    """G7의 인증 상태를 준비하고 선행 관문 초기화에 따른 잠금도 처리한다."""
    if not all_prerequisites_complete() and is_complete("G7"):
        reset_game("G7")
    st.session_state.setdefault("g7_unlocked", False)
    if not all_prerequisites_complete():
        st.session_state["g7_unlocked"] = False


def g7_a() -> None:
    """G7-A: G1~G6가 모두 완료되어야 암호 인증을 진행한다."""
    st.subheader("G7-A | 선행 관문 및 단서 암호 확인")

    for game_id in GAME_IDS[:6]:
        st.write(f"{game_id}: {'완료' if is_complete(game_id) else '미완료'}")

    if not all_prerequisites_complete():
        st.warning("G1~G6를 모두 완료해야 G7을 진행할 수 있습니다.")
        return

    if st.session_state["g7_unlocked"]:
        st.success("암호 확인 완료")
        return

    password = st.text_input(
        "G5와 G6에서 얻은 단서를 이어 붙인 암호",
        type="password",
        key="g7_password",
    )
    if st.button("암호 확인", key="g7_verify"):
        if password.strip() == G7_PASSWORD:
            st.session_state["g7_unlocked"] = True
            complete_game("G7")
            st.rerun()
        else:
            st.error("암호가 틀렸습니다.")


def g7_b() -> None:
    """G7-B: 인증 후 종강 버튼으로 게임 완료 기록 및 내부 상태를 초기화한다."""
    st.subheader("G7-B | 종강 처리 및 전체 초기화")

    if not all_prerequisites_complete() or not st.session_state["g7_unlocked"]:
        st.info("G1~G6를 완료하고 암호를 확인해야 종강 버튼이 활성화됩니다.")
        return

    if st.button("종강 처리하기", type="primary", key="g7_finish"):
        reset_all_games()
        # reset_all_games()는 'g7_' 접두사 상태를 지우므로 별도 키로 안내를 유지한다.
        st.session_state["after_reset_notice"] = "종강 처리 완료: G1~G7 진행 상태가 초기화되었습니다."
        st.rerun()


def render() -> None:
    """app.py가 호출하는 G7 표준 진입 함수."""
    initialize_g7_state()
    st.header("G7 · 종강 버튼의 배신")

    notice = st.session_state.pop("after_reset_notice", None)
    if notice:
        st.success(notice)

    g7_a()
    st.divider()
    g7_b()
