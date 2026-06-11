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
