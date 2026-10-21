"""G6: 기말 범위 기억하기 — 이 파일의 render() 내부에서 실제 게임을 구현하세요."""
import streamlit as st

# 완료 조건 달성 시: from core.state import complete_game
# complete_game("G6")
# 재시작 시: from core.state import reset_game
# reset_game("G6")


def render() -> None:
    st.subheader("G7. 기말 범위 기억하기")
    st.info("G7 모듈 자리입니다. 담당 팀원이 이 파일에 기능을 구현합니다.")
    st.caption("구현 범위: 단어 3개를 5초 동안 보여주고 숨긴 뒤 정답 3개 선택")
