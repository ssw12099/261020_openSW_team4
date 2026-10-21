"""G1 까다로운 출첵봇 (G1-A + G1-B).

이 모듈은 다른 게임 파일 및 app.py와 독립적으로 동작합니다.
- G1-A: 8자리 숫자 학번 + 출석 확인 + 정확한 확인 문구 검증
- G1-B: 같은 학번은 SQLite UNIQUE 제약으로 1회만 저장하고 게임 완료 처리

교수님 자료에는 세부 출석 조건이 지정되어 있지 않아, 체크박스와 확인 문구는
게임 규칙으로 추가했습니다. 원하는 경우 아래 CONFIRM_PHRASE만 수정하세요.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re
import sqlite3

import streamlit as st

from core.state import complete_game, is_complete, reset_game

GAME_ID = "G1"
CONFIRM_PHRASE = "출석합니다"
DATABASE_PATH = Path(__file__).resolve().parents[1] / "data" / "g1_attendance.sqlite3"


def validate_attendance(
    student_id: str, attending: bool, phrase: str
) -> tuple[bool, str]:
    """학번과 출석 조건을 검증합니다 (DB를 건드리지 않는 순수 함수)."""
    if not re.fullmatch(r"[0-9]{8}", student_id.strip()):
        return False, "학번은 공백·하이픈 없이 숫자 8자리여야 해요."
    if not attending:
        return False, "실제 수업에 출석했다는 확인을 체크해 주세요."
    if phrase != CONFIRM_PHRASE:
        return False, f"확인 문구를 정확히 '{CONFIRM_PHRASE}'라고 입력해 주세요."
    return True, "출석 조건을 모두 통과했어요!"


def _initialize_database(connection: sqlite3.Connection) -> None:
    connection.execute(
        """CREATE TABLE IF NOT EXISTS g1_attendance (
               student_id TEXT PRIMARY KEY,
               checked_in_at TEXT NOT NULL
           )"""
    )


def save_attendance(student_id: str, db_path: Path = DATABASE_PATH) -> bool:
    """처음 등록된 학번만 INSERT, 기존 학번은 덮어쓰거나 중복 저장하지 않습니다.

    Returns:
        True: 신규 학번이 저장됨 / False: 이미 저장된 학번
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path, timeout=5) as conn:
        _initialize_database(conn)
        cursor = conn.execute(
            """INSERT OR IGNORE INTO g1_attendance (student_id, checked_in_at)
               VALUES (?, ?)""",
            (student_id, datetime.now(timezone.utc).isoformat(timespec="seconds")),
        )
        return cursor.rowcount == 1


def attendance_count(db_path: Path = DATABASE_PATH) -> int:
    """저장된 학번 개수만 읽습니다 (학번 목록은 화면에 노출하지 않음)."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path, timeout=5) as conn:
        _initialize_database(conn)
        row = conn.execute("SELECT COUNT(*) FROM g1_attendance").fetchone()
    return int(row[0])


def clear_attendance(db_path: Path = DATABASE_PATH) -> None:
    """(데모용) 저장된 출석 기록 전체 삭제. G7 담당자가 필요 시 명시적으로 호출.

    주의: 같은 서버에 접속한 다른 사용자의 기록까지 삭제하므로
    실제 수업 운영 서비스에서는 사용하지 않는 것이 좋습니다.
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path, timeout=5) as conn:
        _initialize_database(conn)
        conn.execute("DELETE FROM g1_attendance")


def render() -> None:
    """메인 app.py가 호출하는 G1 게임 진입점."""
    st.subheader("G1. 까다로운 출첵봇 🤖")
    st.caption("G1-A 학번·출석 조건 판정  ·  G1-B 동일 학번 1회 저장 및 완료 처리")

    st.write("출첵봇의 까다로운 요구를 모두 통과하면 출석을 인정받을 수 있습니다.")
    with st.expander("📋 출첵봇의 규칙", expanded=True):
        st.markdown(
            f"""1. **숫자 8자리** 학번만 인정합니다. (공백·하이픈 불가)
2. **수업에 실제로 참석했음**을 확인해야 합니다.
3. 확인 문구 **`{CONFIRM_PHRASE}`**를 한 글자도 틀리지 않고 입력하세요.
4. **같은 학번은 단 한 번만 저장**됩니다."""
        )

    try:
        st.metric("지금까지 등록된 출석", f"{attendance_count()}명")
    except (sqlite3.Error, OSError) as error:
        st.error("출석 저장소를 열 수 없습니다. 저장 폴더 권한을 확인해 주세요.")
        st.caption(f"오류 종류: {type(error).__name__}")
        return

    if is_complete(GAME_ID):
        st.success("✅ G1 통과! 출석이 완료되었습니다. 다른 관문으로 이동하세요.")
        if st.button("G1 다시 도전", key="g1_reset"):
            reset_game(GAME_ID)  # 개인 진행도만 초기화; 등록된 학번 DB는 보존
            st.rerun()
        st.caption("다시 도전해도 기존 출석 기록은 삭제되지 않습니다.")
        return

    with st.form("g1_attendance_form", clear_on_submit=False):
        student_id = st.text_input(
            "① 학번 8자리",
            max_chars=20,
            placeholder="예: 20261234 (테스트용 가상 학번)",
            key="g1_student_id",
        )
        attending = st.checkbox(
            "② 저는 현재 수업에 참석하고 있습니다.", key="g1_attending"
        )
        phrase = st.text_input(
            "③ 확인 문구 입력",
            placeholder=f"'{CONFIRM_PHRASE}'를 입력하세요",
            key="g1_phrase",
        )
        submitted = st.form_submit_button("🚀 출석 제출", use_container_width=True)

    if submitted:
        valid, message = validate_attendance(student_id, attending, phrase)
        if not valid:
            st.error(f"❌ 출첵봇: {message}")
            return

        try:
            newly_saved = save_attendance(student_id)
        except (sqlite3.Error, OSError) as error:
            st.error("저장 중 오류가 발생했습니다. 잠시 뒤 다시 시도해 주세요.")
            st.caption(f"오류 종류: {type(error).__name__}")
            return

        if not newly_saved:
            st.warning("⚠️ 출첵봇: 이미 출석 처리된 학번입니다. 중복 저장은 불가능합니다.")
            return

        complete_game(GAME_ID)
        st.rerun()  # 사이드바의 완료 표시를 즉시 새로고침
