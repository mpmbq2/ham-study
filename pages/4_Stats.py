import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

from lib.history import (
    compute_history_stats,
    compute_subelement_stats,
    compute_weakest_questions,
)
from lib.session import initialize

load_dotenv()

st.set_page_config(page_title="Stats", page_icon="📊", layout="wide")
initialize()

st.title("Your Stats")

questions = st.session_state.questions
history = st.session_state.history

if not history:
    st.info("No attempts recorded yet. Start with **Random Quiz** or a **Practice Test**.")
    st.stop()

# ── Tier 1: Summary cards ─────────────────────────────────────────────────────
stats = compute_history_stats(history)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Attempts", stats["total_attempts"])
c2.metric("Overall Accuracy", f"{stats['overall_accuracy']:.0%}")
c3.metric("Unique Questions Seen", f"{stats['unique_questions']} / {len(questions)}")
c4.metric("Practice Tests Completed", stats["practice_tests"])

st.divider()

# ── Tier 2: Subelement chart ──────────────────────────────────────────────────
st.subheader("Accuracy by Subelement")

sub_stats = compute_subelement_stats(history, questions)

if sub_stats:
    df = pd.DataFrame(sub_stats)
    df["accuracy_pct"] = (df["accuracy"] * 100).round(1)
    df["color"] = df["accuracy"].apply(
        lambda a: "≥80% (green)" if a >= 0.8 else ("60–79% (yellow)" if a >= 0.6 else "<60% (red)")
    )
    df["label"] = df.apply(
        lambda r: f"{r['accuracy_pct']}%  ({r['attempts']} attempts)", axis=1
    )

    fig = px.bar(
        df,
        x="accuracy_pct",
        y="subelement",
        orientation="h",
        color="color",
        color_discrete_map={
            "≥80% (green)": "#2ecc71",
            "60–79% (yellow)": "#f1c40f",
            "<60% (red)": "#e74c3c",
        },
        text="label",
        labels={"accuracy_pct": "Accuracy (%)", "subelement": ""},
        range_x=[0, 105],
    )
    fig.update_layout(showlegend=False, yaxis={"categoryorder": "total ascending"})
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Tier 3: Weakest questions ─────────────────────────────────────────────────
st.subheader("Weakest Questions (≥3 attempts)")

weak = compute_weakest_questions(history, questions, min_attempts=3, limit=20)

if not weak:
    st.info("No question has been attempted 3 or more times yet. Keep quizzing!")
else:
    q_map = {q["id"]: q for q in questions}
    for w in weak:
        q = q_map.get(w["id"], {})
        header = f"**{w['id']}** ({w['subelement']}) — {w['accuracy']:.0%} accuracy ({w['attempts']} attempts)"
        with st.expander(header):
            st.write(f"**Question:** {q.get('question', '?')}")
            if q:
                st.success(
                    f"**Correct answer:** {q['correct']}. {q['answers'][q['correct']]}"
                )
