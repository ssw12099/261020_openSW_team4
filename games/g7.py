"""G7: 종강 버튼의 배신 — render() 내부에서 실제 게임을 구현합니다."""
import streamlit as st

# 완료 조건 달성 시: from core.state import complete_game
# complete_game("G6")
# 재시작 시: from core.state import reset_game
# reset_game("G6")

def render() -> None:
    st.subheader("G7. 종강 버튼의 배신")
    st.info("G7 모듈 자리입니다. 담당 팀원이 이 파일에 기능을 구현합니다.")
    st.caption("구현 범위: 관문 완료와 단서 암호 검증, 종강 처리, 전체 초기화")
