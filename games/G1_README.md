# G1. 까다로운 출첵봇 🤖

**Python + Streamlit | G1-A·B 통합 모듈 | 의도적 버그 1개 포함**

## 기능
- **G1-A:** 숫자 8자리 학번, 출석 체크, 확인 문구 `출석합니다` 검사
- **G1-B:** SQLite에 학번 최초 1회 저장(중복 방지), 성공하면 `complete_game("G1")` 실행
- `games/g1.py`의 `render()`를 메인 `app.py`에서 호출하며, DB는 `data/g1_attendance.sqlite3`에 생성됨

## 실행
프로젝트 최상위 폴더에서:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

왼쪽에서 **G1** 선택 → 학번 입력 → 출석 체크 → `출석합니다` 입력 → 제출. 실습에는 가상 학번을 사용할 것.

## 🐛 의도적 버그: 학번 공백 처리

**정상 기대:** 숫자 8자리 이외의 학번은 거절, 같은 학번은 한 번만 등록.

**재현:**
1. `20261234`로 정상 출석한다.
2. **G1 다시 도전**을 누른다.
3. `20261234 ` (끝에 공백 1칸)을 입력하고 나머지 조건을 동일하게 제출한다.
4. **실제:** 공백이 붙은 학번도 통과해 신규 출석으로 저장된다.

**원인:** 검증은 `student_id.strip()`으로 공백을 제거하지만, DB에는 공백이 포함된 원본 학번을 저장한다. 따라서 SQLite가 두 학번을 다른 값으로 처리한다.

<details>
<summary>수정 힌트 (테스트 후 펼치기)</summary>

`games/g1.py` → `validate_attendance()`에서:

```python
# 수정 전
re.fullmatch(r"[0-9]{8}", student_id.strip())
# 수정 후: 공백 포함 입력 거절
re.fullmatch(r"[0-9]{8}", student_id)
```

</details>

## 간단 테스트
| 입력/상황 | 기대 결과 |
|---|---|
| `1234` 또는 `2026abcd` | 형식 오류 |
| 체크 안 함 / 확인 문구 오타 | 출석 거절 |
| `20261234` 최초 입력 | 등록 성공 · G1 완료 |
| 같은 학번 재입력 | 중복 차단 |
| `20261234 ` 재입력 | **거절되어야 하지만 현재 버그로 등록됨** |

> **실습 시 주의:** `G1 다시 도전`은 화면 진행 상태만 초기화하며, SQLite 기록은 유지된다. `data/*.sqlite3`와 `data/*.sqlite3-*`는 `.gitignore`에 추가한다. 오류 수정은 `games/g1.py`에서 진행해 공통 `app.py`·`core/state.py`에 영향을 주지 않도록 한다.
