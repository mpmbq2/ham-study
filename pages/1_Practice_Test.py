import streamlit as st
from dotenv import load_dotenv

from lib.history import make_attempt, save_attempts_batch
from lib.questions import sample_exam
from lib.session import initialize

load_dotenv()

st.set_page_config(page_title="Practice Test", page_icon="📝", layout="wide")
initialize()

st.title("Practice Test")

questions = st.session_state.questions
username = st.session_state.username

reveal_mode = st.sidebar.radio(
    "Answer reveal",
    ["Show answers at the end", "Show answers as I go"],
    index=0,
)
reveal_as_you_go = reveal_mode == "Show answers as I go"

if "pt_state" not in st.session_state:
    st.session_state.pt_state = "idle"

# ── IDLE ──────────────────────────────────────────────────────────────────────
if st.session_state.pt_state == "idle":
    st.write(
        "This test has **35 questions** drawn from all subelements, "
        "weighted to match the real General Class exam. You need **26/35** to pass."
    )
    if st.button("Start Test", type="primary"):
        st.session_state.pt_exam = sample_exam(questions)
        st.session_state.pt_index = 0
        st.session_state.pt_answers = {}
        st.session_state.pt_state = "in_progress"
        st.rerun()

# ── IN PROGRESS ───────────────────────────────────────────────────────────────
elif st.session_state.pt_state == "in_progress":
    exam = st.session_state.pt_exam
    idx = st.session_state.pt_index
    question = exam[idx]

    st.progress((idx) / 35, text=f"Question {idx + 1} of 35")
    st.markdown(f"**{question['id']}** — {question['subelement_name']}")
    st.markdown(f"### {question['question']}")

    already_answered = idx in st.session_state.pt_answers

    if not already_answered:
        choice = st.radio(
            "Select your answer:",
            options=list(question["answers"].keys()),
            format_func=lambda k: f"{k}. {question['answers'][k]}",
            key=f"pt_radio_{idx}",
            index=None,
        )
        if st.button("Submit", disabled=choice is None, type="primary"):
            st.session_state.pt_answers[idx] = choice
            st.rerun()
    else:
        user_answer = st.session_state.pt_answers[idx]
        correct = question["correct"]

        for letter, text in question["answers"].items():
            line = f"{letter}. {text}"
            if letter == correct and reveal_as_you_go:
                st.success(f"✅ **{line}** ← correct answer")
            elif letter == user_answer and user_answer != correct and reveal_as_you_go:
                st.error(f"❌ {line} ← your answer")
            else:
                st.write(f"&nbsp;&nbsp;{line}")

        if reveal_as_you_go:
            if user_answer == correct:
                st.success("Correct!")
            else:
                st.error(f"Incorrect. Correct answer: **{correct}. {question['answers'][correct]}**")

        col1, col2 = st.columns([1, 5])
        if idx < 34:
            if col1.button("Next →"):
                st.session_state.pt_index += 1
                st.rerun()
        else:
            if col1.button("Finish Test →", type="primary"):
                attempts = [
                    make_attempt(exam[i]["id"], st.session_state.pt_answers[i], exam[i]["correct"], "practice")
                    for i in range(35)
                ]
                st.session_state.history = save_attempts_batch(username, st.session_state.history, attempts)
                st.session_state.pt_state = "complete"
                st.rerun()

# ── COMPLETE ──────────────────────────────────────────────────────────────────
elif st.session_state.pt_state == "complete":
    exam = st.session_state.pt_exam
    answers = st.session_state.pt_answers
    correct_count = sum(1 for i, q in enumerate(exam) if answers.get(i) == q["correct"])
    passed = correct_count >= 26

    if passed:
        st.success(f"## {correct_count}/35 — Pass ✓")
    else:
        st.error(f"## {correct_count}/35 — Fail ✗  (need 26 to pass)")

    st.markdown("### Question Review")
    for i, q in enumerate(exam):
        user_ans = answers.get(i, "?")
        is_correct = user_ans == q["correct"]
        icon = "✅" if is_correct else "❌"
        with st.expander(f"{icon} {q['id']}: {q['question'][:90]}"):
            st.write(f"**Your answer:** {user_ans}. {q['answers'].get(user_ans, '(none)')}")
            st.write(f"**Correct answer:** {q['correct']}. {q['answers'][q['correct']]}")

    if st.button("Start New Test", type="primary"):
        for key in ["pt_state", "pt_exam", "pt_index", "pt_answers"]:
            st.session_state.pop(key, None)
        st.rerun()
