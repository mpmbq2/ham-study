import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv

from lib.questions import filter_questions, get_subelements
from lib.session import initialize

load_dotenv()

st.set_page_config(page_title="Browse Questions", page_icon="📖", layout="wide")
initialize()

st.title("Browse Questions")

questions = st.session_state.questions
subelements = get_subelements(questions)

selected_sub = st.sidebar.selectbox(
    "Subelement",
    options=["All"] + subelements,
    index=0,
)

search = st.text_input(
    "Search questions and answers",
    placeholder="e.g. frequency, power, antenna",
)

filtered = filter_questions(
    questions,
    subelement=selected_sub if selected_sub != "All" else None,
    search=search.strip() if search.strip() else None,
)

st.caption(f"Showing **{len(filtered)}** of {len(questions)} questions")

for q in filtered:
    with st.container(border=True):
        st.caption(f"**{q['id']}** — {q['subelement_name']}")
        st.markdown(f"**{q['question']}**")
        for letter, text in q["answers"].items():
            st.write(f"  {letter}. {text}")
        if not st.session_state.get(f"revealed_{q['id']}"):
            if st.button("Show Answer", key=f"show_{q['id']}"):
                st.session_state[f"revealed_{q['id']}"] = True
                st.rerun()
        else:
            correct = q["correct"]
            st.success(f"Correct answer: **{correct}. {q['answers'][correct]}**")
