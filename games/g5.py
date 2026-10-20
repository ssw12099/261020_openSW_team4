"""G5: 고장난 계산기 — 이 파일의 render() 내부에서 실제 게임을 구현하세요."""
import streamlit as st

# 완료 조건 달성 시: from core.state import complete_game
# complete_game("G5")
# 재시작 시: from core.state import reset_game
# reset_game("G5")


def render() -> None:
    st.subheader("G5. 고장난 계산기")
    st.info("G5 모듈 자리입니다. 담당 팀원이 이 파일에 기능을 구현합니다.")
    st.caption("구현 범위: 공개한 연산대로 계산하고 3문제 채점·중복 채점 방지")
