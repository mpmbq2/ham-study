# Ham Radio General Class Study Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a multi-page Streamlit study dashboard for the FCC General Class amateur radio license exam with GCS-backed per-user history and four study modes.

**Architecture:** Multi-page Streamlit app using the native `pages/` directory. Pure-Python `lib/` modules (no Streamlit imports) handle questions, GCS history, auth, and session init. Pages are thin — all `st.*` calls live in pages. Question data is a static JSON file with pre-generated Claude explanations committed to the repo.

**Tech Stack:** Python 3.11+, Streamlit ≥1.35, google-cloud-storage, google-auth, pandas, plotly, anthropic (explanation generation only — one-time script), python-dotenv, pytest

---

## File Map

| File | Responsibility |
|------|----------------|
| `app.py` | Landing/home page |
| `pages/1_Practice_Test.py` | Mode 1: 35-question exam simulation |
| `pages/2_Browse.py` | Mode 2: filterable, searchable question reference |
| `pages/3_Random_Quiz.py` | Mode 3: adaptive random quiz with explanations |
| `pages/4_Stats.py` | Stats: accuracy summary, subelement chart, weakest questions |
| `lib/__init__.py` | Empty package marker |
| `lib/auth.py` | `get_username()` — reads Posit Connect header, falls back to "local" |
| `lib/questions.py` | Load dataset, subelement helpers, exam sampling, weighted selection |
| `lib/history.py` | GCS read/write, attempt construction, stats computation |
| `lib/session.py` | `initialize()` — shared session state setup called by every page |
| `scripts/parse_questions.py` | One-time: parse ARRL text pool → JSON |
| `scripts/generate_explanations.py` | One-time: enrich JSON with Claude-generated explanations |
| `data/general_class_questions.json` | Static question dataset (committed to repo) |
| `tests/conftest.py` | Shared pytest fixtures |
| `tests/test_auth.py` | Unit tests for auth.py |
| `tests/test_questions.py` | Unit tests for questions.py |
| `tests/test_history.py` | Unit tests for history.py |
| `tests/test_parse_questions.py` | Unit tests for parse_questions.py |
| `requirements.txt` | Pinned dependencies |
| `.env.example` | Template for local env vars |
| `.gitignore` | Excludes .env, __pycache__, data/pool.txt |
| `.streamlit/config.toml` | Streamlit server config |

---

## Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `lib/__init__.py`
- Create: `tests/__init__.py`
- Create: `scripts/__init__.py`
- Create: `pages/__init__.py`
- Create: `.streamlit/config.toml`

- [ ] **Step 1: Initialize git repo**

```bash
cd /Users/matt/Projects/Development/ham-study
git init
```

- [ ] **Step 2: Create requirements.txt**

```
streamlit>=1.35.0
google-cloud-storage>=2.16.0
google-auth>=2.29.0
pandas>=2.2.0
plotly>=5.20.0
python-dotenv>=1.0.0
anthropic>=0.28.0
pytest>=8.0.0
```

- [ ] **Step 3: Create .env.example**

```
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account","project_id":"your-project","private_key_id":"...","private_key":"-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n","client_email":"...@....iam.gserviceaccount.com","client_id":"...","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token"}
GCS_BUCKET_NAME=ham-study-history
ANTHROPIC_API_KEY=sk-ant-...
```

- [ ] **Step 4: Create .gitignore**

```
.env
__pycache__/
*.pyc
.pytest_cache/
.streamlit/secrets.toml
data/pool.txt
```

- [ ] **Step 5: Create package markers and Streamlit config**

Create these as empty files: `lib/__init__.py`, `tests/__init__.py`, `scripts/__init__.py`, `pages/__init__.py`

Create `.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501

[theme]
base = "light"
```

- [ ] **Step 6: Install dependencies**

```bash
pip install -r requirements.txt
```
Expected: All packages install without error.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt .env.example .gitignore lib/__init__.py tests/__init__.py scripts/__init__.py pages/__init__.py .streamlit/config.toml
git commit -m "chore: project scaffolding"
```
Expected: Clean commit, no errors.

---

## Task 2: Parse FCC Question Pool

**Files:**
- Create: `scripts/parse_questions.py`
- Create: `tests/test_parse_questions.py`
- Create: `data/general_class_questions.json` (output of running the script)

The ARRL publishes the official 2023–2027 General Class question pool at https://www.arrl.org/question-pools. Download the plain-text (.txt) version and save it as `data/pool.txt`. The format uses `~~` as a question separator. Each question block starts with an ID like `G1A01 (D)` where the letter in parentheses is the correct answer.

- [ ] **Step 1: Write the failing test**

Create `tests/test_parse_questions.py`:

```python
from scripts.parse_questions import parse_pool_text

SAMPLE = """SUBELEMENT G1 – COMMISSION'S RULES [5 exam questions – 5 groups]

G1A – General class control operator frequency privileges

G1A01 (D) [97.301(d)]
On which of the following bands is a General class licensee permitted to transmit?
A. 80 meters
B. 40 meters
C. 15 meters
D. None of these choices is correct
~~

G1A02 (A)
What is the maximum transmitting power?
A. 1500 watts PEP output
B. 200 watts PEP output
C. 1000 watts PEP output
D. 100 watts PEP output
~~

SUBELEMENT G2 – OPERATING PROCEDURES [5 exam questions – 5 groups]

G2A – Phone operating procedures

G2A01 (A)
Which sideband is commonly used for voice communications on 17 and 12 meters?
A. Upper sideband
B. Lower sideband
C. AM equivalent sideband
D. Double sideband
~~"""


def test_parse_returns_correct_count():
    questions = parse_pool_text(SAMPLE)
    assert len(questions) == 3


def test_parse_question_id_and_correct_answer():
    questions = parse_pool_text(SAMPLE)
    assert questions[0]["id"] == "G1A01"
    assert questions[0]["correct"] == "D"


def test_parse_answer_choices():
    questions = parse_pool_text(SAMPLE)
    q = questions[0]
    assert len(q["answers"]) == 4
    assert q["answers"]["A"] == "80 meters"
    assert q["answers"]["D"] == "None of these choices is correct"


def test_parse_subelement_assignment():
    questions = parse_pool_text(SAMPLE)
    assert questions[0]["subelement"] == "G1"
    assert questions[2]["subelement"] == "G2"


def test_parse_subelement_name():
    questions = parse_pool_text(SAMPLE)
    assert "COMMISSION" in questions[0]["subelement_name"].upper()
    assert "OPERATING" in questions[2]["subelement_name"].upper()


def test_parse_explanation_starts_empty():
    questions = parse_pool_text(SAMPLE)
    assert questions[0]["explanation"] == ""


def test_parse_skips_blocks_without_question_id():
    # Subelement headers and group headers should not produce questions
    questions = parse_pool_text(SAMPLE)
    assert all(q["id"].startswith("G") and len(q["id"]) == 5 for q in questions)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_parse_questions.py -v
```
Expected: `ImportError` — `scripts.parse_questions` does not exist yet.

- [ ] **Step 3: Implement scripts/parse_questions.py**

```python
import json
import re
import sys
from pathlib import Path


def parse_pool_text(text: str) -> list[dict]:
    questions = []
    current_subelement = None
    current_subelement_name = ""

    for block in text.split("~~"):
        block = block.strip()
        if not block:
            continue

        sub_match = re.search(
            r"SUBELEMENT\s+(G\d)\s*[–\-]\s*(.+?)(?:\s*\[\d+)",
            block,
            re.IGNORECASE,
        )
        if sub_match:
            current_subelement = sub_match.group(1).upper()
            current_subelement_name = sub_match.group(2).strip()

        id_match = re.search(r"^(G\d[A-Z]\d{2})\s*\(([A-D])\)", block, re.MULTILINE)
        if not id_match:
            continue

        question_id = id_match.group(1)
        correct = id_match.group(2)
        subelement = question_id[:2] if current_subelement is None else current_subelement

        lines = [
            ln.strip()
            for ln in block[id_match.end() :].strip().splitlines()
            if ln.strip()
        ]

        answers: dict[str, str] = {}
        question_lines: list[str] = []
        ans_re = re.compile(r"^([A-D])\.\s+(.+)$")

        for line in lines:
            m = ans_re.match(line)
            if m:
                answers[m.group(1)] = m.group(2).strip()
            elif not answers:
                question_lines.append(line)

        question_text = " ".join(question_lines).strip()

        if question_text and len(answers) == 4:
            questions.append(
                {
                    "id": question_id,
                    "subelement": subelement,
                    "subelement_name": current_subelement_name,
                    "question": question_text,
                    "answers": answers,
                    "correct": correct,
                    "explanation": "",
                }
            )

    return questions


def main() -> None:
    pool_path = Path("data/pool.txt")
    if not pool_path.exists():
        print(
            f"ERROR: {pool_path} not found.\n"
            "Download the ARRL 2023-2027 General Class question pool (plain text) "
            "from https://www.arrl.org/question-pools and save it as data/pool.txt"
        )
        sys.exit(1)

    text = pool_path.read_text(encoding="utf-8", errors="replace")
    questions = parse_pool_text(text)
    print(f"Parsed {len(questions)} questions")

    out = Path("data/general_class_questions.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(questions, indent=2, ensure_ascii=False))
    print(f"Written to {out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_parse_questions.py -v
```
Expected: All 7 tests PASS.

- [ ] **Step 5: Download the pool and run the parser**

Download the 2023–2027 General Class pool plain-text file from https://www.arrl.org/question-pools, save as `data/pool.txt`, then:

```bash
python scripts/parse_questions.py
```
Expected output: `Parsed 430 questions` (approximately), `Written to data/general_class_questions.json`.

Verify the output:
```bash
python -c "
import json
qs = json.load(open('data/general_class_questions.json'))
subs = sorted(set(q['subelement'] for q in qs))
print(f'{len(qs)} questions, subelements: {subs}')
"
```
Expected: ~430 questions, subelements `['G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9']`.

- [ ] **Step 6: Commit**

```bash
git add scripts/parse_questions.py tests/test_parse_questions.py data/general_class_questions.json
git commit -m "feat: parse ARRL General Class question pool to JSON"
```

---

## Task 3: Generate Explanations

**Files:**
- Create: `scripts/generate_explanations.py`

This is a one-time enrichment step. Requires `ANTHROPIC_API_KEY` in `.env`. Reads `data/general_class_questions.json`, calls Claude Haiku for each question without an explanation, and writes results back. Saves progress every 25 questions so it can resume if interrupted.

- [ ] **Step 1: Create scripts/generate_explanations.py**

```python
import json
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

_PROMPT = """\
You are an expert ham radio instructor. A student is studying for the FCC General Class license exam.

Question: {question}
A. {A}
B. {B}
C. {C}
D. {D}
Correct answer: {correct}. {correct_text}

In 2–3 sentences, explain why {correct} is correct and why the other choices are wrong. Be specific and educational. Do not start with "The correct answer is"."""


def _explain(client: anthropic.Anthropic, q: dict) -> str:
    prompt = _PROMPT.format(
        question=q["question"],
        A=q["answers"]["A"],
        B=q["answers"]["B"],
        C=q["answers"]["C"],
        D=q["answers"]["D"],
        correct=q["correct"],
        correct_text=q["answers"][q["correct"]],
    )
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def main() -> None:
    data_path = Path("data/general_class_questions.json")
    questions: list[dict] = json.loads(data_path.read_text())
    client = anthropic.Anthropic()

    pending = [q for q in questions if not q.get("explanation")]
    print(f"{len(pending)} questions need explanations (out of {len(questions)} total)")

    for i, q in enumerate(questions):
        if q.get("explanation"):
            continue
        print(f"[{i + 1}/{len(questions)}] {q['id']}", end="  ", flush=True)
        try:
            q["explanation"] = _explain(client, q)
            print("OK")
        except Exception as exc:
            print(f"ERROR: {exc}")
            q["explanation"] = ""
        time.sleep(0.3)

        if (i + 1) % 25 == 0:
            data_path.write_text(json.dumps(questions, indent=2, ensure_ascii=False))
            print(f"  — saved progress ({i + 1} done)")

    data_path.write_text(json.dumps(questions, indent=2, ensure_ascii=False))
    print("Done.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Copy your Anthropic API key into .env**

Create `.env` (not committed):
```
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_APPLICATION_CREDENTIALS_JSON=...
GCS_BUCKET_NAME=ham-study-history
```

- [ ] **Step 3: Run the explanation generator**

```bash
python scripts/generate_explanations.py
```
Expected: Prints one line per question (`[1/430] G1A01  OK`), saves progress every 25. Takes approximately 8–12 minutes. Each API call costs ~$0.0004 (Haiku pricing); total ~$0.17.

- [ ] **Step 4: Verify all explanations are populated**

```bash
python -c "
import json
qs = json.load(open('data/general_class_questions.json'))
missing = [q['id'] for q in qs if not q.get('explanation')]
print(f'{len(missing)} missing explanations')
if missing:
    print('First 5:', missing[:5])
"
```
Expected: `0 missing explanations`.

- [ ] **Step 5: Commit enriched dataset**

```bash
git add data/general_class_questions.json scripts/generate_explanations.py
git commit -m "feat: add Claude-generated explanations to question dataset"
```

---

## Task 4: lib/auth.py

**Files:**
- Create: `lib/auth.py`
- Create: `tests/conftest.py`
- Create: `tests/test_auth.py`

- [ ] **Step 1: Write failing tests**

Create `tests/conftest.py`:

```python
import pytest


@pytest.fixture
def sample_questions():
    return [
        {
            "id": "G1A01",
            "subelement": "G1",
            "subelement_name": "Commission's Rules",
            "question": "Which band is permitted?",
            "answers": {"A": "80m", "B": "40m", "C": "15m", "D": "None"},
            "correct": "A",
            "explanation": "80m is correct because it falls within General privileges.",
        },
        {
            "id": "G1A02",
            "subelement": "G1",
            "subelement_name": "Commission's Rules",
            "question": "What is the maximum power?",
            "answers": {"A": "100W", "B": "200W", "C": "500W", "D": "1500W"},
            "correct": "D",
            "explanation": "1500W PEP is the maximum for General class.",
        },
        {
            "id": "G2A01",
            "subelement": "G2",
            "subelement_name": "Operating Procedures",
            "question": "Which sideband for HF voice?",
            "answers": {"A": "USB", "B": "LSB", "C": "AM", "D": "FM"},
            "correct": "A",
            "explanation": "USB is standard above 10 MHz for SSB voice.",
        },
    ]


@pytest.fixture
def sample_history():
    return [
        {
            "question_id": "G1A01",
            "user_answer": "A",
            "correct_answer": "A",
            "correct": True,
            "timestamp": "2026-06-10T12:00:00+00:00",
            "mode": "random",
        },
        {
            "question_id": "G1A01",
            "user_answer": "B",
            "correct_answer": "A",
            "correct": False,
            "timestamp": "2026-06-10T12:01:00+00:00",
            "mode": "random",
        },
        {
            "question_id": "G1A02",
            "user_answer": "D",
            "correct_answer": "D",
            "correct": True,
            "timestamp": "2026-06-10T12:02:00+00:00",
            "mode": "practice",
        },
    ]
```

Create `tests/test_auth.py`:

```python
from lib.auth import get_username


def test_returns_posit_connect_username(monkeypatch):
    monkeypatch.setenv("HTTP_X_RSTUDIO_CONNECT_USER_NAME", "jsmith")
    assert get_username() == "jsmith"


def test_lowercases_username(monkeypatch):
    monkeypatch.setenv("HTTP_X_RSTUDIO_CONNECT_USER_NAME", "JSmith")
    assert get_username() == "jsmith"


def test_falls_back_to_local(monkeypatch):
    monkeypatch.delenv("HTTP_X_RSTUDIO_CONNECT_USER_NAME", raising=False)
    assert get_username() == "local"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_auth.py -v
```
Expected: `ImportError` — `lib.auth` not found.

- [ ] **Step 3: Implement lib/auth.py**

```python
import os


def get_username() -> str:
    username = os.environ.get("HTTP_X_RSTUDIO_CONNECT_USER_NAME")
    if username:
        return username.lower()
    return "local"
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_auth.py -v
```
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add lib/auth.py tests/test_auth.py tests/conftest.py
git commit -m "feat: add auth module for Posit Connect user identification"
```

---

## Task 5: lib/questions.py

**Files:**
- Create: `lib/questions.py`
- Create: `tests/test_questions.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_questions.py`:

```python
import pytest
from lib.questions import (
    compute_accuracy,
    filter_questions,
    get_subelements,
    sample_exam,
    weighted_sample,
)


def test_get_subelements_sorted_and_unique(sample_questions):
    doubled = sample_questions + sample_questions
    subs = get_subelements(doubled)
    assert subs == ["G1", "G2"]
    assert len(subs) == len(set(subs))


def test_compute_accuracy_empty_history(sample_questions):
    assert compute_accuracy(sample_questions, []) == {}


def test_compute_accuracy(sample_questions, sample_history):
    acc = compute_accuracy(sample_questions, sample_history)
    assert acc["G1A01"] == pytest.approx(0.5)
    assert acc["G1A02"] == pytest.approx(1.0)
    assert "G2A01" not in acc


def test_weighted_sample_favors_unseen(sample_questions, sample_history):
    counts = {q["id"]: 0 for q in sample_questions}
    for _ in range(500):
        q = weighted_sample(sample_questions, sample_history)
        counts[q["id"]] += 1
    # G2A01 is unseen (weight 1.0), should dominate
    assert counts["G2A01"] > counts["G1A01"]
    assert counts["G2A01"] > counts["G1A02"]


def test_weighted_sample_pure_random_visits_all(sample_questions, sample_history):
    counts = {q["id"]: 0 for q in sample_questions}
    for _ in range(300):
        q = weighted_sample(sample_questions, sample_history, pure_random=True)
        counts[q["id"]] += 1
    assert all(c > 0 for c in counts.values())


def test_filter_by_subelement(sample_questions):
    result = filter_questions(sample_questions, subelement="G1")
    assert all(q["subelement"] == "G1" for q in result)
    assert len(result) == 2


def test_filter_by_search_question_text(sample_questions):
    result = filter_questions(sample_questions, search="band")
    assert len(result) >= 1
    assert all(
        "band" in q["question"].lower()
        or any("band" in v.lower() for v in q["answers"].values())
        for q in result
    )


def test_filter_no_criteria_returns_all(sample_questions):
    assert len(filter_questions(sample_questions)) == len(sample_questions)


def test_sample_exam_returns_35():
    pool = []
    exam_counts = {
        "G1": 5, "G2": 3, "G3": 3, "G4": 5, "G5": 3,
        "G6": 2, "G7": 3, "G8": 3, "G9": 4, "G0": 4,
    }
    for sub, count in exam_counts.items():
        for i in range(count * 3):
            pool.append({
                "id": f"{sub}A{i:02d}",
                "subelement": sub,
                "subelement_name": f"{sub} Name",
                "question": f"Question {sub} {i}?",
                "answers": {"A": "a", "B": "b", "C": "c", "D": "d"},
                "correct": "A",
                "explanation": "",
            })
    exam = sample_exam(pool)
    assert len(exam) == 35


def test_sample_exam_respects_subelement_counts():
    pool = []
    exam_counts = {
        "G1": 5, "G2": 3, "G3": 3, "G4": 5, "G5": 3,
        "G6": 2, "G7": 3, "G8": 3, "G9": 4, "G0": 4,
    }
    for sub, count in exam_counts.items():
        for i in range(count * 3):
            pool.append({
                "id": f"{sub}A{i:02d}",
                "subelement": sub,
                "subelement_name": f"{sub} Name",
                "question": f"Q?",
                "answers": {"A": "a", "B": "b", "C": "c", "D": "d"},
                "correct": "A",
                "explanation": "",
            })
    exam = sample_exam(pool)
    by_sub = {}
    for q in exam:
        by_sub[q["subelement"]] = by_sub.get(q["subelement"], 0) + 1
    for sub, expected in exam_counts.items():
        assert by_sub.get(sub, 0) == expected, f"{sub}: expected {expected}, got {by_sub.get(sub, 0)}"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_questions.py -v
```
Expected: `ImportError` — `lib.questions` not found.

- [ ] **Step 3: Implement lib/questions.py**

```python
import json
import random
from pathlib import Path

_QUESTIONS_PATH = Path(__file__).parent.parent / "data" / "general_class_questions.json"

_EXAM_COUNTS = {
    "G1": 5, "G2": 3, "G3": 3, "G4": 5, "G5": 3,
    "G6": 2, "G7": 3, "G8": 3, "G9": 4, "G0": 4,
}


def load_questions() -> list[dict]:
    with open(_QUESTIONS_PATH) as f:
        return json.load(f)


def get_subelements(questions: list[dict]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for q in questions:
        if q["subelement"] not in seen:
            seen.add(q["subelement"])
            result.append(q["subelement"])
    return sorted(result)


def filter_questions(
    questions: list[dict],
    subelement: str | None = None,
    search: str | None = None,
) -> list[dict]:
    result = questions
    if subelement:
        result = [q for q in result if q["subelement"] == subelement]
    if search:
        term = search.lower()
        result = [
            q for q in result
            if term in q["question"].lower()
            or any(term in v.lower() for v in q["answers"].values())
        ]
    return result


def compute_accuracy(questions: list[dict], history: list[dict]) -> dict[str, float]:
    correct: dict[str, int] = {}
    total: dict[str, int] = {}
    for attempt in history:
        qid = attempt["question_id"]
        total[qid] = total.get(qid, 0) + 1
        if attempt["correct"]:
            correct[qid] = correct.get(qid, 0) + 1
    return {qid: correct.get(qid, 0) / cnt for qid, cnt in total.items()}


def weighted_sample(
    questions: list[dict],
    history: list[dict],
    pure_random: bool = False,
) -> dict:
    if pure_random:
        return random.choice(questions)
    accuracy = compute_accuracy(questions, history)
    weights = [max(1.0 - accuracy.get(q["id"], 0.0), 0.05) for q in questions]
    return random.choices(questions, weights=weights, k=1)[0]


def sample_exam(questions: list[dict]) -> list[dict]:
    by_sub: dict[str, list[dict]] = {}
    for q in questions:
        by_sub.setdefault(q["subelement"], []).append(q)
    exam: list[dict] = []
    for sub, count in _EXAM_COUNTS.items():
        pool = by_sub.get(sub, [])
        exam.extend(random.sample(pool, min(count, len(pool))))
    random.shuffle(exam)
    return exam
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_questions.py -v
```
Expected: All 10 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add lib/questions.py tests/test_questions.py
git commit -m "feat: add questions module with sampling, filtering, and accuracy"
```

---

## Task 6: lib/history.py

**Files:**
- Create: `lib/history.py`
- Create: `tests/test_history.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_history.py`:

```python
import json
import pytest
from unittest.mock import MagicMock, patch

from lib.history import (
    compute_history_stats,
    compute_subelement_stats,
    compute_weakest_questions,
    load_history,
    make_attempt,
    save_attempt,
    save_attempts_batch,
)


def _mock_bucket(exists=True, data=None):
    blob = MagicMock()
    blob.exists.return_value = exists
    if data is not None:
        blob.download_as_text.return_value = json.dumps(data)
    bucket = MagicMock()
    bucket.blob.return_value = blob
    return bucket, blob


def test_make_attempt_correct():
    a = make_attempt("G1A01", "A", "A", "random")
    assert a["question_id"] == "G1A01"
    assert a["user_answer"] == "A"
    assert a["correct_answer"] == "A"
    assert a["correct"] is True
    assert a["mode"] == "random"
    assert "timestamp" in a


def test_make_attempt_incorrect():
    a = make_attempt("G1A01", "B", "A", "practice")
    assert a["correct"] is False
    assert a["mode"] == "practice"


def test_load_history_returns_empty_when_no_file():
    bucket, _ = _mock_bucket(exists=False)
    with patch("lib.history._get_bucket", return_value=bucket):
        assert load_history("testuser") == []


def test_load_history_returns_data(sample_history):
    bucket, _ = _mock_bucket(exists=True, data=sample_history)
    with patch("lib.history._get_bucket", return_value=bucket):
        assert load_history("testuser") == sample_history


def test_load_history_uses_correct_path():
    bucket, _ = _mock_bucket(exists=False)
    with patch("lib.history._get_bucket", return_value=bucket):
        load_history("jsmith")
    bucket.blob.assert_called_once_with("history/jsmith.json")


def test_save_attempt_appends_and_uploads(sample_history):
    bucket, blob = _mock_bucket()
    new_attempt = make_attempt("G2A01", "C", "A", "random")
    with patch("lib.history._get_bucket", return_value=bucket):
        result = save_attempt("testuser", sample_history, new_attempt)
    assert len(result) == len(sample_history) + 1
    assert result[-1] == new_attempt
    uploaded = json.loads(blob.upload_from_string.call_args[0][0])
    assert len(uploaded) == len(sample_history) + 1


def test_save_attempts_batch_single_upload(sample_history):
    bucket, blob = _mock_bucket()
    new_attempts = [
        make_attempt("G2A01", "A", "A", "practice"),
        make_attempt("G3A01", "B", "B", "practice"),
    ]
    with patch("lib.history._get_bucket", return_value=bucket):
        result = save_attempts_batch("testuser", sample_history, new_attempts)
    assert len(result) == len(sample_history) + 2
    blob.upload_from_string.assert_called_once()


def test_compute_history_stats_empty():
    stats = compute_history_stats([])
    assert stats["total_attempts"] == 0
    assert stats["overall_accuracy"] == 0.0
    assert stats["unique_questions"] == 0
    assert stats["practice_tests"] == 0


def test_compute_history_stats(sample_history):
    stats = compute_history_stats(sample_history)
    assert stats["total_attempts"] == 3
    assert stats["overall_accuracy"] == pytest.approx(2 / 3)
    assert stats["unique_questions"] == 2


def test_compute_subelement_stats(sample_history, sample_questions):
    stats = compute_subelement_stats(sample_history, sample_questions)
    g1 = next(s for s in stats if s["subelement"] == "G1")
    assert g1["attempts"] == 3
    assert g1["accuracy"] == pytest.approx(2 / 3)


def test_compute_weakest_questions_min_attempts_filter(sample_history, sample_questions):
    # G1A01 has 2 attempts, G1A02 has 1 — neither reaches 3
    result = compute_weakest_questions(sample_history, sample_questions, min_attempts=3)
    assert result == []


def test_compute_weakest_questions_sorted_by_accuracy(sample_history, sample_questions):
    result = compute_weakest_questions(sample_history, sample_questions, min_attempts=1)
    # G1A01 at 50% should come before G1A02 at 100%
    assert result[0]["id"] == "G1A01"
    assert result[0]["accuracy"] == pytest.approx(0.5)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_history.py -v
```
Expected: `ImportError` — `lib.history` not found.

- [ ] **Step 3: Implement lib/history.py**

```python
import json
import os
from collections import defaultdict
from datetime import datetime, timezone

from dotenv import load_dotenv
from google.cloud import storage
from google.oauth2 import service_account

load_dotenv()


def _get_bucket():
    creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if creds_json:
        info = json.loads(creds_json)
        creds = service_account.Credentials.from_service_account_info(
            info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        client = storage.Client(credentials=creds, project=info.get("project_id"))
    else:
        client = storage.Client()
    bucket_name = os.environ.get("GCS_BUCKET_NAME", "ham-study-history")
    return client.bucket(bucket_name)


def load_history(username: str) -> list[dict]:
    bucket = _get_bucket()
    blob = bucket.blob(f"history/{username}.json")
    if not blob.exists():
        return []
    return json.loads(blob.download_as_text())


def _write_history(username: str, history: list[dict]) -> None:
    bucket = _get_bucket()
    blob = bucket.blob(f"history/{username}.json")
    blob.upload_from_string(
        json.dumps(history, ensure_ascii=False),
        content_type="application/json",
    )


def save_attempt(username: str, history: list[dict], attempt: dict) -> list[dict]:
    updated = history + [attempt]
    _write_history(username, updated)
    return updated


def save_attempts_batch(
    username: str, history: list[dict], attempts: list[dict]
) -> list[dict]:
    updated = history + attempts
    _write_history(username, updated)
    return updated


def make_attempt(
    question_id: str, user_answer: str, correct_answer: str, mode: str
) -> dict:
    return {
        "question_id": question_id,
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "correct": user_answer == correct_answer,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
    }


def compute_history_stats(history: list[dict]) -> dict:
    if not history:
        return {
            "total_attempts": 0,
            "overall_accuracy": 0.0,
            "unique_questions": 0,
            "practice_tests": 0,
        }
    correct = sum(1 for a in history if a["correct"])
    unique = len(set(a["question_id"] for a in history))
    practice_count = sum(1 for a in history if a["mode"] == "practice")
    return {
        "total_attempts": len(history),
        "overall_accuracy": correct / len(history),
        "unique_questions": unique,
        "practice_tests": practice_count // 35,
    }


def compute_subelement_stats(history: list[dict], questions: list[dict]) -> list[dict]:
    q_to_sub = {q["id"]: q["subelement"] for q in questions}
    correct_by_sub: dict[str, int] = defaultdict(int)
    total_by_sub: dict[str, int] = defaultdict(int)
    for attempt in history:
        sub = q_to_sub.get(attempt["question_id"])
        if sub:
            total_by_sub[sub] += 1
            if attempt["correct"]:
                correct_by_sub[sub] += 1
    return [
        {
            "subelement": sub,
            "attempts": total_by_sub[sub],
            "accuracy": correct_by_sub[sub] / total_by_sub[sub],
        }
        for sub in sorted(total_by_sub.keys())
    ]


def compute_weakest_questions(
    history: list[dict],
    questions: list[dict],
    min_attempts: int = 3,
    limit: int = 20,
) -> list[dict]:
    q_map = {q["id"]: q for q in questions}
    correct_by_q: dict[str, int] = defaultdict(int)
    total_by_q: dict[str, int] = defaultdict(int)
    for attempt in history:
        qid = attempt["question_id"]
        total_by_q[qid] += 1
        if attempt["correct"]:
            correct_by_q[qid] += 1
    result = []
    for qid, total in total_by_q.items():
        if total < min_attempts:
            continue
        q = q_map.get(qid, {})
        result.append(
            {
                "id": qid,
                "subelement": q.get("subelement", "?"),
                "question": q.get("question", "?"),
                "attempts": total,
                "accuracy": correct_by_q[qid] / total,
            }
        )
    return sorted(result, key=lambda x: x["accuracy"])[:limit]
```

- [ ] **Step 4: Run full test suite**

```bash
pytest -v
```
Expected: All tests PASS (test_auth, test_questions, test_history, test_parse_questions).

- [ ] **Step 5: Commit**

```bash
git add lib/history.py tests/test_history.py
git commit -m "feat: add history module with GCS persistence and stats computation"
```

---

## Task 7: lib/session.py and app.py

**Files:**
- Create: `lib/session.py`
- Create: `app.py`

`lib/session.py` provides a single `initialize()` function that every page calls to ensure questions, username, and history are in session state. This prevents errors when users land on a page directly without visiting home first.

- [ ] **Step 1: Create lib/session.py**

```python
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
```

- [ ] **Step 2: Create app.py**

```python
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
```

- [ ] **Step 3: Start the app and verify it loads**

Ensure `.env` has `GOOGLE_APPLICATION_CREDENTIALS_JSON` and `GCS_BUCKET_NAME`, then:

```bash
streamlit run app.py
```
Expected: App loads at `http://localhost:8501`. Shows username "local", question count (~430), and 0 attempts. No terminal errors.

- [ ] **Step 4: Commit**

```bash
git add lib/session.py app.py
git commit -m "feat: add session initializer and landing page"
```

---

## Task 8: Practice Test Page

**Files:**
- Create: `pages/1_Practice_Test.py`

- [ ] **Step 1: Create pages/1_Practice_Test.py**

```python
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
```

- [ ] **Step 2: Verify in browser**

Navigate to "Practice Test" in sidebar. Verify:
- "Start Test" button appears; clicking it loads question 1 of 35 with a progress bar
- Radio buttons show all four answer choices
- Submit is disabled until an answer is selected
- With "Show answers as I go": correct/incorrect feedback appears after submit
- With "Show answers at the end": no feedback until results screen
- After question 35, "Finish Test" writes attempts and shows results
- Results screen shows pass/fail with 26/35 threshold and expandable per-question review
- After finishing, Stats page shows increased attempt count

- [ ] **Step 3: Commit**

```bash
git add pages/1_Practice_Test.py
git commit -m "feat: add practice test mode"
```

---

## Task 9: Browse Page

**Files:**
- Create: `pages/2_Browse.py`

- [ ] **Step 1: Create pages/2_Browse.py**

```python
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
            st.write(f"  {letter}. {text}")
        if not st.session_state.get(f"revealed_{q['id']}"):
            if st.button("Show Answer", key=f"show_{q['id']}"):
                st.session_state[f"revealed_{q['id']}"] = True
                st.rerun()
        else:
            correct = q["correct"]
            st.success(f"Correct answer: **{correct}. {q['answers'][correct]}**")
```

- [ ] **Step 2: Verify in browser**

Navigate to "Browse". Verify:
- Subelement selectbox (sidebar) filters questions; "All" shows everything
- Typing in the search box filters questions matching the text
- Combining subelement + search applies both filters
- "Show Answer" button reveals the correct answer with green highlight; it stays revealed while on the page
- No history is recorded while browsing

- [ ] **Step 3: Commit**

```bash
git add pages/2_Browse.py
git commit -m "feat: add browse mode with subelement filter and keyword search"
```

---

## Task 10: Random Quiz Page

**Files:**
- Create: `pages/3_Random_Quiz.py`

- [ ] **Step 1: Create pages/3_Random_Quiz.py**

```python
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
        key=f"rq_radio_{question['id']}",
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
            st.write(f"  {line}")

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
```

- [ ] **Step 2: Verify in browser**

Navigate to "Random Quiz". Verify:
- A question loads immediately on page visit
- Submit is disabled until an answer is selected
- Correct answer: all choices shown, correct one highlighted green, "Correct!" message
- Incorrect answer: red highlight on your answer, green on correct, explanation expander auto-opens
- Sidebar shows session accuracy updating after each answer
- "Next Question" loads a new question; explanation resets
- Toggling "Pure random" changes selection behavior (no weighting)

- [ ] **Step 3: Commit**

```bash
git add pages/3_Random_Quiz.py
git commit -m "feat: add random quiz mode with weakness weighting and explanations"
```

---

## Task 11: Stats Page

**Files:**
- Create: `pages/4_Stats.py`

- [ ] **Step 1: Create pages/4_Stats.py**

```python
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
```

- [ ] **Step 2: Verify in browser**

After completing at least one practice test and several random quiz questions, navigate to "Stats". Verify:
- Four metric cards show correct totals
- Subelement bar chart renders with correct colors (green ≥80%, yellow 60–79%, red <60%)
- After ≥3 attempts on any question, the weakest questions section populates
- Expanders show the correct answer for each weak question

- [ ] **Step 3: Commit**

```bash
git add pages/4_Stats.py
git commit -m "feat: add stats dashboard with subelement chart and weakest questions"
```

---

## Task 12: End-to-End Smoke Test and Deployment Prep

**Files:**
- No new files — verification and deployment config only

- [ ] **Step 1: Run full test suite**

```bash
pytest -v
```
Expected: All tests PASS. Output ends with something like `X passed in Y.Zs`.

- [ ] **Step 2: Full app smoke test**

Start the app:
```bash
streamlit run app.py
```

Walk through every mode:

1. **Home page**: question count shows ~430, attempts = 0 for a fresh local run
2. **Practice Test**: start a test, answer all 35 questions in reveal-as-you-go mode, finish, verify score and review table appear, verify Stats page shows +35 attempts
3. **Practice Test**: start again in end-only mode, answer a few questions, navigate forward/back not possible (intentional), finish
4. **Browse**: select G1 from sidebar — only G1 questions shown; type "frequency" in search — further filtered; click "Show Answer" on a question — correct answer highlighted green; it stays visible
5. **Random Quiz**: answer 5 questions; verify wrong answers show explanation; verify sidebar session accuracy updates; toggle "Pure random" on and off
6. **Stats**: verify all four metric cards, subelement chart renders without error, weakest questions section appears after enough attempts

- [ ] **Step 3: Deploy to Posit Connect**

In Posit Connect dashboard:
1. Create a new deployment pointing to this repository
2. Set environment variables in the app's **Vars** tab:
   - `GOOGLE_APPLICATION_CREDENTIALS_JSON` — paste the full service account JSON as a single-line string
   - `GCS_BUCKET_NAME` — your GCS bucket name
3. Publish and open the app
4. Verify the landing page shows your Posit Connect username (not "local")
5. Complete a short quiz session and verify history persists across page refreshes

- [ ] **Step 4: Final commit**

```bash
git add -A
git status  # confirm only expected files are staged
git commit -m "chore: verified deployment-ready"
```
