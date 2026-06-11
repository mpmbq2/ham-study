import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv

from lib.history import make_attempt, save_attempt
from lib.questions import weighted_sample
from lib.session import initialize

load_dotenv()

st.set_page_config(page_title="Random Quiz", page_icon="🎯", layout="wide")
initialize()

st.title("Random Quiz")

questions = st.session_state.questions
username = st.session_state.username

pure_random = st.sidebar.toggle("Pure random (ignore weakness weighting)", value=False)

if "rq_session_total" not in st.session_state:
    st.session_state.rq_session_total = 0
if "rq_session_correct" not in st.session_state:
    st.session_state.rq_session_correct = 0

total = st.session_state.rq_session_total
correct = st.session_state.rq_session_correct

if total > 0:
    st.sidebar.metric(
        "Session accuracy",
        f"{correct / total:.0%}",
        f"{total} answered this session",
    )
else:
    st.sidebar.caption("No questions answered this session yet.")

if "rq_question" not in st.session_state:
    st.session_state.rq_question = weighted_sample(
        questions, st.session_state.history, pure_random=pure_random
    )
    st.session_state.rq_submitted = False

question = st.session_state.rq_question
submitted = st.session_state.rq_submitted

st.markdown(f"**{question['id']}** — {question['subelement_name']}")
st.markdown(f"### {question['question']}")

if not submitted:
    choice = st.radio(
        "Select your answer:",
        options=list(question["answers"].keys()),
        format_func=lambda k: f"{k}. {question['answers'][k]}",
        key=f"rq_radio_{st.session_state.rq_session_total}_{question['id']}",
        index=None,
    )
    if st.button("Submit", disabled=choice is None, type="primary"):
        correct_ans = question["correct"]
        is_correct = choice == correct_ans
        attempt = make_attempt(question["id"], choice, correct_ans, "random")
        st.session_state.history = save_attempt(username, st.session_state.history, attempt)
        st.session_state.rq_last_choice = choice
        st.session_state.rq_submitted = True
        st.session_state.rq_session_total += 1
        if is_correct:
            st.session_state.rq_session_correct += 1
        st.rerun()
else:
    user_answer = st.session_state.rq_last_choice
    correct_ans = question["correct"]
    is_correct = user_answer == correct_ans

    for letter, text in question["answers"].items():
        line = f"{letter}. {text}"
        if letter == correct_ans:
            st.success(f"✅ **{line}** ← correct answer")
        elif letter == user_answer and not is_correct:
            st.error(f"❌ {line} ← your answer")
        else:
            st.write(f"  {line}")

    if is_correct:
        st.success("Correct!")
    else:
        st.error("Incorrect.")
        with st.expander("Why is this the correct answer?", expanded=True):
            st.write(question.get("explanation") or "No explanation available.")

    if st.button("Next Question →", type="primary"):
        st.session_state.rq_question = weighted_sample(
            questions, st.session_state.history, pure_random=pure_random
        )
        st.session_state.rq_submitted = False
        if "rq_last_choice" in st.session_state:
            del st.session_state["rq_last_choice"]
        st.rerun()
