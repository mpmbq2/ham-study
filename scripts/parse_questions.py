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
            for ln in block[id_match.end():].strip().splitlines()
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
