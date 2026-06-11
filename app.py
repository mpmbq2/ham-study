import streamlit as st
from dotenv import load_dotenv

from lib.session import initialize

load_dotenv()

st.set_page_config(
    page_title="Ham Radio General Class Study",
    page_icon="📻",
    layout="wide",
)

initialize()

questions = st.session_state.questions
username = st.session_state.username
history = st.session_state.history

st.title("Ham Radio General Class Study")
st.caption(f"Logged in as: **{username}**")

c1, c2, c3 = st.columns(3)
c1.metric("Questions in Pool", len(questions))
c2.metric("Attempts Recorded", len(history))
c3.metric("Unique Questions Seen", len(set(a["question_id"] for a in history)))

st.markdown("""
---
## Study Modes

Use the sidebar to navigate between modes:

| Mode | Description |
|------|-------------|
| **Practice Test** | 35 questions matching the real General Class exam structure |
| **Browse** | Browse all 430+ questions by subelement or search by keyword |
| **Random Quiz** | Adaptive one-at-a-time quiz — focuses on your weak areas |
| **Stats** | Your accuracy breakdown by subelement and question |
""")
