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
