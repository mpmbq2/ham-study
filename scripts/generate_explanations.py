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
    data_path = Path(__file__).parent.parent / "data" / "general_class_questions.json"
    if not data_path.exists():
        print(
            f"ERROR: {data_path} not found.\n"
            "Run scripts/parse_questions.py first to generate the question dataset."
        )
        return

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
