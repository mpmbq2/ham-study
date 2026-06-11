# Ham Radio General Class Study Dashboard — Design Spec

**Date:** 2026-06-10  
**Status:** Approved

---

## Overview

A Streamlit multi-page dashboard for studying the FCC Amateur Radio General Class (Element 3) license exam. The app provides four study modes backed by a static question dataset and per-user attempt history stored in Google Cloud Storage. Deployed privately on Posit Connect.

---

## Architecture

Multi-page Streamlit app using the native `pages/` directory structure. Shared logic lives in a `lib/` package with no Streamlit imports — pages are thin and handle all `st.*` calls, `lib/` modules are pure Python.

```
ham-study/
├── app.py                              # Landing/home page
├── pages/
│   ├── 1_Practice_Test.py
│   ├── 2_Browse.py
│   ├── 3_Random_Quiz.py
│   └── 4_Stats.py
├── lib/
│   ├── questions.py                    # Load & parse question dataset
│   ├── history.py                      # GCS read/write for attempt history
│   └── auth.py                         # Credentials + Posit Connect username
├── data/
│   └── general_class_questions.json    # Full question pool with explanations
├── requirements.txt
└── .env                                # Local only, gitignored
```

**Session state initialization:** `app.py` initializes the GCS client and loads the user's history from GCS on first load, storing both in `st.session_state`. All pages access these via session state — no redundant GCS calls.

---

## Data Layer

### Question Dataset

`data/general_class_questions.json` — static JSON array, one object per question (~430 total). Sourced from the official FCC 2023–2027 General Class question pool. Explanations pre-generated via Claude and stored statically (no runtime LLM calls).

```json
{
  "id": "G1A01",
  "subelement": "G1",
  "subelement_name": "Commission's Rules",
  "question": "On which of the following bands is a General class licensee...",
  "answers": {
    "A": "60 meters",
    "B": "30 meters",
    "C": "17 meters",
    "D": "12 meters"
  },
  "correct": "A",
  "explanation": "The correct answer is A because..."
}
```

Loaded once at startup via `st.cache_data`.

### Attempt History

Stored in GCS at `history/{username}.json` — one file per user, keyed by Posit Connect session username. JSON array of attempt records, appended on each answer submission.

```json
{
  "question_id": "G1A01",
  "user_answer": "B",
  "correct_answer": "A",
  "correct": false,
  "timestamp": "2026-06-10T14:32:00Z",
  "mode": "random"
}
```

`history.py` loads the full file once per session into `st.session_state`. Writes overwrite the full file (files stay under ~50KB even after thousands of attempts). GCS bucket and credentials are configured via environment variables.

### Authentication & Credentials

- **GCS credentials:** Full service account JSON stored as `GOOGLE_APPLICATION_CREDENTIALS_JSON` environment variable. Parsed at runtime via `google.oauth2.service_account.Credentials.from_service_account_info()`.
- **Local dev:** `.env` file (gitignored) + `python-dotenv`.
- **Posit Connect:** Env vars set in the Connect dashboard under the app's Vars settings.
- **Per-user namespacing:** Posit Connect passes the authenticated username via the `X-RStudio-Connect-User-Name` HTTP header (Python env: `HTTP_X_RSTUDIO_CONNECT_USER_NAME`). `auth.py` reads this header to key GCS history files. Falls back to `"local"` in dev.

---

## Mode 1 — Practice Test

Mirrors the real General Class exam: **35 questions** sampled from all 9 subelements using the official per-subelement counts (G1: 5, G2: 3, G3: 3, G4: 5, G5: 3, G6: 2, G7: 3, G8: 3, G9: 4, G0: 4).

**Flow:**
1. "Start Test" button samples questions into `st.session_state` for the test duration.
2. Sidebar toggle: **"Show answers as I go"** vs **"Show all answers at the end"**.
3. One question at a time with progress indicator (`Question 12 of 35`).
4. In reveal-as-you-go mode: correct/incorrect feedback after each answer, then "Next."
5. In end-only mode: no feedback until after question 35.
6. **Results screen:** score (e.g., `28/35 — Pass`), pass/fail indicator (threshold: 26/35), table of all questions with user answer vs. correct answer.
7. All 35 attempts written to history with `"mode": "practice"`.

No back-navigation — answers locked once submitted.

---

## Mode 2 — Browse

Read-only study reference. No history recorded.

**Layout:**
- Sidebar selectbox: subelement filter (G1–G9 or "All").
- Search bar: keyword filter across question text and answer text. Combines with subelement filter.
- Question cards: question ID, question text, all four answer choices (A–D). Answers hidden by default — "Show Answer" button per card reveals the correct answer highlighted in green (one-way, not a toggle).
- No explanations shown (reserved for Mode 3 wrong-answer learning moments).

~430 questions rendered without pagination. `st.cache_data` on question loader ensures single parse.

---

## Mode 3 — Random Quiz

Primary adaptive study mode. One question at a time, runs indefinitely.

**Question selection:**
- Default: **weakness-weighted** — `weight = 1 - accuracy_rate`, unseen questions get weight `1.0`. Weighted random draw each turn.
- Sidebar toggle: **"Pure random"** — uniform sampling.

**Flow per question:**
1. Question and four answer choices displayed as radio buttons.
2. User selects an answer and clicks "Submit."
3. **Correct:** green confirmation, correct answer highlighted.
4. **Incorrect:** red indicator, correct answer highlighted, explanation panel shown.
5. Attempt written to history with `"mode": "random"`.
6. "Next Question" button loads the next question.

Sidebar mini-stat shows questions answered and accuracy % since the current Streamlit session started (resets on page refresh).

---

## Stats View

**Tier 1 — Summary cards:**
- Total attempts (all-time)
- Overall accuracy rate
- Unique questions seen (out of 430)
- Practice tests completed

**Tier 2 — Subelement accuracy chart:**
- Horizontal bar chart, one bar per subelement G1–G9
- Bar = accuracy %; color-coded green (≥80%), yellow (60–79%), red (<60%)
- Attempt count per subelement shown as secondary label

**Tier 3 — Weakest questions table:**
- Questions with ≥3 attempts, sorted by accuracy ascending
- Columns: Question ID, Subelement, Question (truncated), Attempts, Accuracy %
- Capped at 20 rows
- `st.expander` per row to show full question and correct answer

Stats computed fresh from history on each page render (no caching).

---

## Dependencies

```
streamlit
google-cloud-storage
google-auth
pandas
plotly
python-dotenv
```

---

## Deployment

- **Platform:** Posit Connect (private)
- **Credentials:** `GOOGLE_APPLICATION_CREDENTIALS_JSON` and `GCS_BUCKET_NAME` as Connect env vars
- **GCS bucket:** one bucket, `history/` prefix for user history files
- **Local dev:** `.env` file with same vars, `python-dotenv` loads on startup
