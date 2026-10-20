"""G6: 기말 범위 기억하기 — 단어 5초 노출(G6-A), 3개 선택(G6-B)."""

import math
import random
import time

import streamlit as st

from core.state import is_complete, mark_complete

G6_WORD_POOL = ("행성", "연필", "시계", "우산", "노트", "사과", "기차", "바다")
G6_EXPOSURE_SECONDS = 5


def initialize_g6_state() -> None:
    """G6 게임별 상태만 초기화한다."""
    defaults = {
        "g6_started_at": None,
        "g6_targets": [],
        "g6_options": [],
        "g6_round": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, list) else value


def g6_a() -> bool:
    """G6-A: 5초 노출이 끝났으면 True, 그렇지 않으면 False."""
    st.subheader("G6-A | 단어 3개를 5초 노출 후 숨김")

    if is_complete("G6"):
        st.success("G6 관문 완료. 단서 2: **빛**")
        return False

    started_at = st.session_state["g6_started_at"]
    if started_at is None:
        st.write("시작하면 무작위 단어 3개가 5초간 나타납니다.")
        if st.button("암기 시작", key="g6_start"):
            st.session_state["g6_targets"] = random.sample(G6_WORD_POOL, 3)
            st.session_state["g6_options"] = random.sample(G6_WORD_POOL, len(G6_WORD_POOL))
            st.session_state["g6_started_at"] = time.monotonic()
            st.rerun(scope="fragment")
        return False

    seconds_left = G6_EXPOSURE_SECONDS - (time.monotonic() - started_at)
    if seconds_left > 0:
        st.info("　 | 　".join(st.session_state["g6_targets"]))
        st.caption(f"남은 암기 시간: {math.ceil(seconds_left)}초")
        return False

    st.write("5초가 지나 단어가 숨겨졌습니다.")
    return True


def g6_b() -> None:
    """G6-B: 정답 3개만 선택하면 G6 완료로 기록한다."""
    st.subheader("G6-B | 정답 3개만 선택하면 완료")
    selected = st.multiselect(
        "앞에서 본 단어 3개를 선택하세요.",
        options=st.session_state["g6_options"],
        max_selections=3,
        key=f"g6_selected_{st.session_state['g6_round']}",
    )

    if len(selected) == 3:
        if set(selected) == set(st.session_state["g6_targets"]):
            mark_complete("G6")
            st.rerun()  # 전체 페이지를 새로 그려 사이드바 진행률도 갱신한다.
        else:
            st.error("정답이 아닌 단어가 포함되어 있습니다. 다시 선택하세요.")

    if st.button("다시 암기하기", key="g6_retry"):
        st.session_state["g6_round"] += 1
        st.session_state["g6_started_at"] = None
        st.session_state["g6_targets"] = []
        st.session_state["g6_options"] = []
        st.rerun(scope="fragment")


@st.fragment(run_every="1s")
def render() -> None:
    """app.py에서 호출하는 G6 표준 진입 함수. 암기 중 1초마다 갱신."""
    initialize_g6_state()
    st.header("G6 · 기말 범위 기억하기")
    ready_for_quiz = g6_a()
    if ready_for_quiz:
        st.divider()
        g6_b()
