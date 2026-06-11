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
