"""G3: 최신 공식 공지를 선택하고 강의 장소와 시간을 맞히는 게임."""
import streamlit as st
from core.state import complete_game, is_complete, reset_game

# 실제 공지가 아닌 게임용 예시. 게시 시각은 동일한 시간대입니다.
NOTICES = (
    dict(id="A", source="학과 게시판", official=True, posted="2026-10-19 09:00",
         title="보강 안내", place="공학관 201호", time="14:00"),
    dict(id="B", source="학생 단체 채팅방", official=False, posted="2026-10-20 12:00",
         title="보강 장소가 바뀌었다던데?", place="학생회관 101호", time="16:00"),
    dict(id="C", source="교수님 LMS", official=True, posted="2026-10-20 10:00",
         title="[정정] 보강 장소·시간 변경", place="공학관 305호", time="15:00"),
    dict(id="D", source="학과 게시판", official=True, posted="2026-10-20 08:30",
         title="보강 시간 변경", place="공학관 201호", time="15:00"),
)


def render() -> None:
    st.subheader("G3. 수상한 강의 공지")
    st.caption("아래 공지는 모두 게임용 예시입니다.")
    st.write("최신 공식 공지를 찾은 뒤, 10월 21일 보강 장소와 시작 시간을 맞혀 보세요.")

    if st.button("G3 다시 시작", key="g3_restart"):
        reset_game("G3")
        st.rerun()

    if is_complete("G3"):
        st.success("G3 완료! 최신 공식 공지의 장소와 시간을 모두 맞혔습니다.")
        return

    latest = max((n for n in NOTICES if n["official"]), key=lambda n: n["posted"])
    for notice in NOTICES:
        with st.expander(f"공지 {notice['id']} · {notice['title']}", expanded=True):
            category = "공식" if notice["official"] else "비공식"
            st.caption(f"{category} | {notice['source']} | 게시: {notice['posted']}")
            st.write(f"10월 21일 보강: {notice['place']}, {notice['time']} 시작")

    if not st.session_state.get("g3_notice_verified", False):
        st.write("**1단계 · 최신 공식 공지 선택**")
        with st.form("g3_notice_form"):
            selected = st.radio(
                "따라야 할 공지는 무엇인가요?", options=[n["id"] for n in NOTICES],
                index=None, format_func=lambda value: f"공지 {value}",
                key="g3_notice_choice",
            )
            submitted = st.form_submit_button("공지 확인")
        if submitted:
            if selected is None:
                st.warning("공지를 하나 선택해 주세요.")
            elif selected != latest["id"]:
                st.error("공식 출처인지 확인하고, 공식 공지끼리 게시 시각을 비교해 보세요.")
            else:
                st.session_state["g3_notice_verified"] = True
                st.rerun()
        return

    st.success(f"공지 {latest['id']}가 최신 공식 공지입니다.")
    st.write("**2단계 · 장소와 시간 확인**")
    with st.form("g3_answer_form"):
        place = st.selectbox(
            "보강 장소", options=list(dict.fromkeys(n["place"] for n in NOTICES)),
            index=None, placeholder="장소를 선택하세요", key="g3_place",
        )
        time = st.selectbox(
            "보강 시작 시간", options=sorted({n["time"] for n in NOTICES}),
            index=None, placeholder="시간을 선택하세요", key="g3_time",
        )
        submitted = st.form_submit_button("정답 제출")
    if submitted:
        if place is None or time is None:
            st.warning("장소와 시간을 모두 선택해 주세요.")
        elif place == latest["place"] and time == latest["time"]:
            complete_game("G3")
            st.rerun()
        else:
            st.error("장소 또는 시간이 맞지 않습니다. 최신 공식 공지를 다시 확인해 보세요.")
