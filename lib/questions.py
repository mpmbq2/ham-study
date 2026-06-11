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
