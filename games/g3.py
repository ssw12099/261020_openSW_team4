"""G3: 수상한 강의 공지 — 이 파일의 render() 내부에서 실제 게임을 구현하세요."""
import streamlit as st

# 완료 조건 달성 시: from core.state import complete_game
# complete_game("G3")
# 재시작 시: from core.state import reset_game
# reset_game("G3")


def render() -> None:
    st.subheader("G3. 수상한 강의 공지")
    st.info("G3 모듈 자리입니다. 담당 팀원이 이 파일에 기능을 구현합니다.")
    st.caption("구현 범위: 최신 공지 선택 후 장소·시간 정답 판정")
