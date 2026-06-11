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
