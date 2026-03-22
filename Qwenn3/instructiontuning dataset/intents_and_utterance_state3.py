import json
import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

# -----------------------------
# Config
# -----------------------------
INPUT_FILE = "restaurant_dataset.jsonl"
OUTPUT_FILE = "state3_extracted.jsonl"


# -----------------------------
# Helpers
# -----------------------------
def safe_literal_eval(text: str) -> Any:
    try:
        return ast.literal_eval(text.strip())
    except Exception:
        return None


def normalize_filled(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(x) for x in value]
    if isinstance(value, dict):
        return [str(k) for k in value.keys()]
    return []


def normalize_missing(value: Any) -> List[str]:
    if isinstance(value, list):
        return [str(x) for x in value]
    return []


def extract_from_system(system_text: str) -> Optional[Dict[str, Any]]:
    """
    Expected patterns:
    Intent: choose_pickup. Filled: ['food_item']. Missing: ['quantity', 'pickup_time'].
    or
    Intent: choose_pickup. Filled: {'food_item': '...'} . Missing: ['quantity', 'pickup_time'].
    """
    intent_match = re.search(r"Intent:\s*([^.]+)", system_text)
    filled_match = re.search(r"Filled:\s*(.*?)(?=\.\s*Missing:|$)", system_text)
    missing_match = re.search(r"Missing:\s*(.*?)(?=\.\s*[A-Z][a-zA-Z ]*:|$)", system_text)

    if not intent_match:
        return None

    intent = intent_match.group(1).strip()

    filled_raw = filled_match.group(1).strip() if filled_match else "[]"
    missing_raw = missing_match.group(1).strip() if missing_match else "[]"

    filled_value = safe_literal_eval(filled_raw)
    missing_value = safe_literal_eval(missing_raw)

    return {
        "intent": intent,
        "filled": normalize_filled(filled_value),
        "missing": normalize_missing(missing_value),
    }


def extract_row(row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    messages = row.get("messages")
    if not isinstance(messages, list):
        return None

    system_text = None
    user_text = None

    for msg in messages:
        if not isinstance(msg, dict):
            continue

        role = msg.get("role")
        content = msg.get("content")

        if not isinstance(content, str):
            continue

        if role == "system" and system_text is None:
            system_text = content
        elif role == "user" and user_text is None:
            user_text = content

    if not system_text or not user_text:
        return None

    parsed = extract_from_system(system_text)
    if not parsed:
        return None

    return {
        "intent": parsed["intent"],
        "filled": parsed["filled"],
        "missing": parsed["missing"],
        "user": user_text.strip(),
    }


# -----------------------------
# Main
# -----------------------------
def run():
    input_path = Path(INPUT_FILE)
    if not input_path.exists():
        print(f"Missing input file: {INPUT_FILE}")
        return

    total_in = 0
    total_out = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as fin, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as fout:

        for line_no, line in enumerate(fin, start=1):
            line = line.strip()
            if not line:
                continue

            total_in += 1
            print(f"Processing line {line_no}")

            try:
                row = json.loads(line)
            except Exception as e:
                print(f"Bad JSON at line {line_no}: {e}")
                continue

            extracted = extract_row(row)
            if not extracted:
                print(f"No extraction for line {line_no}")
                continue

            fout.write(json.dumps(extracted, ensure_ascii=False) + "\n")
            total_out += 1

    print(f"Done. Read {total_in} rows, wrote {total_out} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()