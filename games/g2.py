"""G2 청개구리 퀴즈 — G2-A(지시/반대 OX), G2-B(3문항 채점/완료/재시작).

팀 공통 app.py에서 games.g2.render()를 호출합니다.
이 버전에는 팀의 Issue/PR 테스트를 위한 의도적 채점 결함 1개가 포함되어 있습니다.
"""

from __future__ import annotations

import streamlit as st

from core.state import complete_game, is_complete, reset_game

GAME_ID = "G2"

# fact_answer: 문장을 있는 그대로 판단했을 때의 참(O)/거짓(X)
QUESTIONS = (
    {
        "id": "q1",
        "mode": "지시대로",
        "statement": "Python은 프로그래밍 언어이다.",
        "fact_answer": "O",
    },
    {
        "id": "q2",
        "mode": "반대로",
        "statement": "Streamlit은 Python으로 웹 앱을 만들 수 있게 해 준다.",
        "fact_answer": "O",
    },
    {
        "id": "q3",
        "mode": "반대로",
        "statement": "Python에서 1 + 1의 결과는 3이다.",
        "fact_answer": "X",
    },
)


def expected_answer(question: dict[str, str]) -> str:
    """현재 게임의 O/X 채점 기준을 계산합니다."""
    answer = question["fact_answer"]
    if question["mode"] == "반대로" and answer == "O":
        return "X"
    return answer


def grade_answers(answers: tuple[str, str, str]) -> tuple[int, tuple[bool, ...]]:
    """3개 답변의 점수와 문항별 채점 여부를 반환합니다."""
    if len(answers) != len(QUESTIONS):
        raise ValueError("정확히 3개의 답안을 제출해야 합니다.")
    if any(answer not in ("O", "X") for answer in answers):
        raise ValueError("각 문항에는 O 또는 X를 선택해야 합니다.")

    correct = tuple(
        answer == expected_answer(question)
        for answer, question in zip(answers, QUESTIONS)
    )
    return sum(correct), correct


def _show_result() -> None:
    result = st.session_state["g2_result"]
    score = result["score"]
    st.metric("이번 도전 점수", f"{score} / 3점")

    if is_complete(GAME_ID):
        st.success("🎉 3점 만점! G2 통과입니다. 다른 관문에 도전하세요!")
    else:
        st.warning("🐸 청개구리에게 졌어요! 3점 만점을 받아야 통과합니다.")

    st.table(
        [
            {
                "문항": f"{number}번",
                "지시": question["mode"],
                "내 답": result["answers"][number - 1],
                "채점 정답": expected_answer(question),
                "결과": "정답" if result["correct"][number - 1] else "오답",
            }
            for number, question in enumerate(QUESTIONS, start=1)
        ]
    )

    if st.button("🔄 G2 다시 시작", key="g2_restart", use_container_width=True):
        reset_game(GAME_ID)
        st.rerun()


def render() -> None:
    """팀 메인 앱에서 호출하는 G2 게임 진입점."""
    st.subheader("G2. 청개구리 퀴즈 🐸")
    st.caption("G2-A 지시대로/반대로 OX 판정 · G2-B 3문항 채점 및 재시작")

    st.markdown(
        "**지시대로** = 문장의 참/거짓을 그대로 선택  ·  "
        "**반대로** = 참이면 X, 거짓이면 O를 선택"
    )
    st.info("3문제를 모두 맞혀야 다음 관문으로 넘어갈 수 있습니다. (3점 만점)")

    if "g2_result" in st.session_state:
        _show_result()
        return

    # G2 완료 표시만 남아 있는 예외적인 경우에도 다시 시작할 수 있습니다.
    if is_complete(GAME_ID):
        st.success("✅ 이미 G2를 통과했습니다.")
        if st.button("🔄 G2 다시 시작", key="g2_restart", use_container_width=True):
            reset_game(GAME_ID)
            st.rerun()
        return

    with st.form("g2_quiz_form"):
        answers = []
        for number, question in enumerate(QUESTIONS, start=1):
            st.markdown(f"#### {number}번 · {question['mode']}")
            st.write(question["statement"])
            choice = st.radio(
                f"{number}번 답 선택",
                options=("O", "X"),
                index=None,
                horizontal=True,
                key=f"g2_answer_{number}",
            )
            answers.append(choice)
            if number != len(QUESTIONS):
                st.divider()

        submitted = st.form_submit_button("📝 3문항 채점하기", use_container_width=True)

    if submitted:
        if any(answer is None for answer in answers):
            st.error("3문항 모두 O 또는 X를 선택해 주세요.")
            return

        score, correct = grade_answers(tuple(answers))
        st.session_state["g2_result"] = {
            "answers": tuple(answers),
            "score": score,
            "correct": correct,
        }
        if score == 3:
            complete_game(GAME_ID)
        st.rerun()
