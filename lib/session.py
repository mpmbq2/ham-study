import streamlit as st

from lib.auth import get_username
from lib.history import load_history
from lib.questions import load_questions


@st.cache_data
def _load_questions_cached() -> list[dict]:
    return load_questions()


def initialize() -> None:
    if "questions" not in st.session_state:
        st.session_state.questions = _load_questions_cached()
    if "username" not in st.session_state:
        st.session_state.username = get_username()
    if "history" not in st.session_state:
        with st.spinner("Loading your study history..."):
            st.session_state.history = load_history(st.session_state.username)
