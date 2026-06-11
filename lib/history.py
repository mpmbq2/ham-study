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
