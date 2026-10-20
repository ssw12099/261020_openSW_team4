"""G5: 고장난 계산기 — 규칙 공개(G5-A)와 3문제 채점(G5-B)."""

import streamlit as st

from core.state import is_complete, mark_complete

G5_PROBLEMS = (
    ("8 + 3", 24),  # + 기호를 곱셈으로 해석한다.
    ("9 - 2", 11),  # - 기호를 덧셈으로 해석한다.
    ("6 × 4", 2),  # × 기호를 뺄셈으로 해석한다.
)


def initialize_g5_state() -> None:
    """G5의 게임별 상태만 초기화한다."""
    defaults = {
        "g5_attempt": 0,
        "g5_graded": False,
        "g5_score": None,
        "g5_pass": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def g5_a() -> None:
    """G5-A: 바뀐 계산 기호 규칙을 설명한다."""
    st.subheader("G5-A | 공개된 바뀐 연산 규칙")
    st.write("계산기에 표시되는 기호의 뜻이 바뀌었습니다.")
    st.info("`+` → 곱셈(×)　 /　 `-` → 덧셈(+)　 /　 `×` → 뺄셈(-)")


def g5_b() -> None:
    """G5-B: 한 시도당 한 번만 채점하며 3/3 정답이면 완료."""
    st.subheader("G5-B | 3문제 채점, 중복 채점 차단")
    attempt = st.session_state["g5_attempt"]
    graded = st.session_state["g5_graded"]

    with st.form(f"g5_form_{attempt}"):
        answers = []
        for i, (question, _) in enumerate(G5_PROBLEMS, start=1):
            answers.append(
                st.number_input(
                    f"문제 {i}. {question} = ?",
                    value=0,
                    step=1,
                    disabled=graded,
                    key=f"g5_answer_{attempt}_{i}",
                )
            )
        submitted = st.form_submit_button("채점하기", disabled=graded)

    if submitted and not st.session_state["g5_graded"]:
        score = sum(
            answer == correct
            for answer, (_, correct) in zip(answers, G5_PROBLEMS)
        )
        st.session_state["g5_score"] = score
        st.session_state["g5_graded"] = True
        if score == len(G5_PROBLEMS):
            st.session_state["g5_pass"] = True
            mark_complete("G5")
        st.rerun()

    if st.session_state["g5_graded"]:
        score = st.session_state["g5_score"]
        if is_complete("G5"):
            st.success(f"{score}/3 정답! G5 완료. 단서 1: **별**")
        else:
            st.error(f"{score}/3 정답. 같은 시도의 중복 채점은 차단됩니다.")
            if st.button("다시 도전하기", key="g5_retry"):
                st.session_state["g5_attempt"] += 1
                st.session_state["g5_graded"] = False
                st.session_state["g5_score"] = None
                st.rerun()


def render() -> None:
    """app.py에서 호출하는 G5 표준 진입 함수."""
    initialize_g5_state()
    st.header("G5 · 고장난 계산기")
    g5_a()
    st.divider()
    g5_b()
