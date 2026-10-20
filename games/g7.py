"""G7: 종강 버튼의 배신 — 관문·암호 검사(G7-A), 전체 초기화(G7-B)."""

import streamlit as st

from core.state import is_complete, mark_complete, reset_all_state

G7_PASSWORD = "별빛"  # G5의 '별' + G6의 '빛'


def initialize_g7_state() -> None:
    """G7 자체 인증 상태만 초기화한다."""
    st.session_state.setdefault("g7_unlocked", False)


def g7_a() -> None:
    """G7-A: G5/G6 완료 후 두 단서의 암호를 확인한다."""
    st.subheader("G7-A | 관문 완료와 단서 암호 검증")
    g5_done = is_complete("G5")
    g6_done = is_complete("G6")
    st.write(f"G5 계산기: {'완료' if g5_done else '미완료'}")
    st.write(f"G6 단어 기억: {'완료' if g6_done else '미완료'}")

    if not (g5_done and g6_done):
        st.warning("G5와 G6 관문을 모두 완료해야 암호를 검증할 수 있습니다.")
        return

    if st.session_state["g7_unlocked"]:
        st.success("암호 검증 완료")
        return

    password = st.text_input(
        "단서 1과 단서 2를 이어 붙인 암호",
        type="password",
        key="g7_password",
    )
    if st.button("암호 확인", key="g7_verify"):
        if password.strip() == G7_PASSWORD:
            st.session_state["g7_unlocked"] = True
            mark_complete("G7")
            st.rerun()  # 사이드바 진행률 표시도 갱신한다.
        else:
            st.error("암호가 틀렸습니다.")


def g7_b() -> None:
    """G7-B: 종강 버튼을 누르면 G1~G7 완료 상태까지 모두 초기화한다."""
    st.subheader("G7-B | 종강 처리, 전체 초기화")
    if not st.session_state["g7_unlocked"]:
        st.info("암호 검증 후 종강 버튼을 사용할 수 있습니다.")
        return

    if st.button("종강 처리하기", type="primary", key="g7_finish"):
        reset_all_state()
        st.session_state["g7_reset_message"] = "종강 처리가 완료되어 G1~G7 진행 상태가 초기화되었습니다."
        st.rerun()


def render() -> None:
    """app.py에서 호출하는 G7 표준 진입 함수."""
    initialize_g7_state()
    st.header("G7 · 종강 버튼의 배신")
    notice = st.session_state.pop("g7_reset_message", None)
    if notice:
        st.success(notice)
    g7_a()
    st.divider()
    g7_b()
