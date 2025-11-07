import random
import streamlit as st


def generate_questions(n=3):
    """곱셈 또는 나눗셈 문제를 n개 생성합니다.

    나눗셈 문제는 항상 정수 정답이 되도록 생성합니다.
    """
    qs = []
    for _ in range(n):
        if random.choice(["mul", "div"]) == "mul":
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            qs.append((f"{a} × {b}", a * b))
        else:
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            prod = a * b
            # 문제는 "prod ÷ a" 로 내서 정답이 b 가 되도록 함
            qs.append((f"{prod} ÷ {a}", b))
    return qs


st.title("✏️ 간단한 곱셈·나눗셈 연습")
st.write("3문제를 연속으로 풀고, 마지막에 정답/오답과 총점을 보여줍니다.")

# 세션 상태 초기화
if "questions" not in st.session_state:
    st.session_state.questions = generate_questions(3)
    st.session_state.qindex = 0
    st.session_state.results = []  # (문제, 사용자가 입력한 값, 정답, 맞았는지)

def submit_answer(user_input: str):
    idx = st.session_state.qindex
    q_text, correct = st.session_state.questions[idx]
    try:
        # 정답은 정수지만 사용자가 실수로 입력할 수도 있으므로 float로 파싱
        user_val = float(user_input)
    except Exception:
        st.error("숫자를 입력해 주세요.")
        return

    # 정답 비교: 정수 정답이므로 정수 비교가 안전
    is_correct = abs(user_val - float(correct)) < 1e-9
    st.session_state.results.append((q_text, user_input, correct, is_correct))
    st.session_state.qindex += 1


if st.session_state.qindex < len(st.session_state.questions):
    i = st.session_state.qindex
    q_text, _ = st.session_state.questions[i]
    st.subheader(f"문제 {i+1} / {len(st.session_state.questions)}")
    st.write(f"문제: {q_text}")

    with st.form(key=f"form_{i}"):
        answer = st.text_input("정답을 입력하세요", key=f"input_{i}")
        submitted = st.form_submit_button("제출")
        if submitted:
            submit_answer(answer)
            st.experimental_rerun()

else:
    st.subheader("결과")
    correct_count = sum(1 for r in st.session_state.results if r[3])
    st.write(f"총 {len(st.session_state.results)}문제 중 {correct_count}문제 정답!")

    for q_text, user_input, correct, is_correct in st.session_state.results:
        if is_correct:
            st.success(f"✅ {q_text} — 당신: {user_input} — 정답: {correct}")
        else:
            st.error(f"❌ {q_text} — 당신: {user_input} — 정답: {correct}")

    if st.button("다시하기"):
        # 상태 초기화 후 새로 고침
        del st.session_state.questions
        del st.session_state.qindex
        del st.session_state.results
        st.experimental_rerun()

