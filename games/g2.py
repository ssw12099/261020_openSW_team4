"""G2: 청개구리 퀴즈 — 이 파일의 render() 내부에서 실제 게임을 구현하세요."""
import streamlit as st

# 완료 조건 달성 시: from core.state import complete_game
# complete_game("G2")
# 재시작 시: from core.state import reset_game
# reset_game("G2")


def render() -> None:
    st.subheader("G2. 청개구리 퀴즈")
    st.info("G2 모듈 자리입니다. 담당 팀원이 이 파일에 기능을 구현합니다.")
    st.caption("구현 범위: 지시대로 또는 반대로 O/X를 판정하고, 3문항 채점 및 재시작 구현")
