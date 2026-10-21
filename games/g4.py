"""G4: 세 번의 협상에서 4점 이상을 얻으면 완료하는 게임."""
import streamlit as st
from core.state import complete_game, is_complete, reset_game


# 사진의 기능 조건을 바탕으로 구성한 게임용 대사와 배점입니다.
ROUNDS = (
    {
        "situation": "팀원이 ‘이번 주는 바쁘니까 내 자료 조사도 대신 해 줘.’라고 합니다.",
        "choices": (
            ("알겠어. 네 몫까지 내가 전부 할게.", 0, "일을 모두 떠안아 역할 분담이 무너졌습니다."),
            ("그럼 가능한 시간에 참고 자료 하나라도 찾아 줘.", 1, "참여를 이끌었지만 역할과 기한이 불명확합니다."),
            ("일정을 확인해서 역할을 조정하자. 맡을 수 있는 분량과 기한을 정해 줘.", 2, "상황을 고려하면서 역할과 기한을 구체적으로 정했습니다."),
        ),
    },
    {
        "situation": "약속한 제출 시간이 지났는데 팀원이 ‘아직 못 했어. 나중에 보낼게.’라고 합니다.",
        "choices": (
            ("지금까지 한 부분을 공유해 줘. 남은 분량과 새 마감 시간을 같이 정하자.", 2, "진행 상황을 확인하고 실행 가능한 마감을 정했습니다."),
            ("괜찮아. 끝나면 아무 때나 보내 줘.", 0, "새 기한이 없어 전체 일정이 밀릴 수 있습니다."),
            ("오늘 안에는 꼭 보내 줘.", 1, "기한은 정했지만 진행 상황과 가능한 분량을 확인하지 못했습니다."),
        ),
    },
    {
        "situation": "발표 전날 팀원이 ‘나는 발표 못 하겠어. 너희끼리 해.’라고 합니다.",
        "choices": (
            ("그럼 발표 자료 검토라도 해 줘.", 1, "대체 역할을 제안했지만 구체적인 작업 약속이 부족합니다."),
            ("어려운 이유를 듣고 짧은 발표나 예상 질문 정리 중 가능한 역할과 기한을 정하자.", 2, "어려움을 확인하고 구체적인 기여 방법을 합의했습니다."),
            ("너는 빠져. 우리가 알아서 할게.", 0, "협상이 끝나고 나머지 팀원의 부담이 커졌습니다."),
        ),
    },
)


def render() -> None:
    st.subheader("G4. 팀플 빌런과 협상")
    st.caption("구현 범위: 3회 선택의 점수 갱신, 4점 이상 성공, 종료와 재시작")
    st.write("팀원과 세 번 협상하세요. 선택마다 0~2점을 얻고, 총 6점 중 4점 이상이면 성공합니다.")
    st.button("G4 다시 시작", key="g4_restart", on_click=reset_game, args=("G4",))

    if "g4_answers" not in st.session_state:
        st.session_state["g4_answers"] = []
    answers = st.session_state["g4_answers"]
    score = sum(ROUNDS[i]["choices"][answer][1] for i, answer in enumerate(answers))
    st.metric("협상 점수", f"{score} / 6")
    st.progress(len(answers) / len(ROUNDS))

    for i, answer in enumerate(answers):
        label, points, feedback = ROUNDS[i]["choices"][answer]
        with st.expander(f"{i + 1}차 협상 결과 · +{points}점", expanded=i == len(answers) - 1):
            st.write(f"선택: {label}")
            st.write(feedback)

    if len(answers) == len(ROUNDS):
        if is_complete("G4"):
            st.success(f"협상 성공! 최종 {score}점으로 G4를 완료했습니다.")
        else:
            st.error(f"협상 종료! 최종 {score}점으로 성공 기준인 4점에 도달하지 못했습니다.")
            st.info("위의 ‘G4 다시 시작’ 버튼으로 다시 도전하세요.")
        return

    step = len(answers)
    current = ROUNDS[step]
    st.write(f"**{step + 1} / 3차 협상**")
    st.write(current["situation"])
    with st.form(f"g4_round_{step}"):
        choice = st.radio(
            "어떻게 대답할까요?",
            options=range(len(current["choices"])),
            format_func=lambda value: current["choices"][value][0],
            index=None,
            key=f"g4_choice_{step}",
        )
        submitted = st.form_submit_button("선택 확정")
    if submitted:
        if choice is None:
            st.warning("대답을 하나 선택해 주세요.")
        else:
            st.session_state["g4_answers"] = [*answers, choice]
            new_score = score + current["choices"][choice][1]
            if step + 1 == len(ROUNDS) and new_score >= 4:
                complete_game("G4")
            st.rerun()
