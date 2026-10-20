"""G4: 팀플 빌런과 협상 — 이 파일의 render() 내부에서 실제 게임을 구현하세요."""
import streamlit as st

# 완료 조건 달성 시: from core.state import complete_game
# complete_game("G4")
# 재시작 시: from core.state import reset_game
# reset_game("G4")


def render() -> None:
    st.subheader("G4. 팀플 빌런과 협상")
    st.info("G4 모듈 자리입니다. 담당 팀원이 이 파일에 기능을 구현합니다.")
    st.caption("구현 범위: 3회 선택 점수 갱신 및 성공 조건·재시작 구현")
