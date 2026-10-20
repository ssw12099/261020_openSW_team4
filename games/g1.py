"""G1: 까다로운 출첵봇 — 이 파일의 render() 내부에서 실제 게임을 구현하세요."""
import streamlit as st

# 완료 조건 달성 시: from core.state import complete_game
# complete_game("G1")
# 재시작 시: from core.state import reset_game
# reset_game("G1")


def render() -> None:
    st.subheader("G1. 까다로운 출첵봇")
    st.info("G1 모듈 자리입니다. 담당 팀원이 이 파일에 기능을 구현합니다.")
    st.caption("구현 범위: 학번 8자리 및 출석 조건을 판정하고, 동일 학번 1회 저장 후 완료 처리")
