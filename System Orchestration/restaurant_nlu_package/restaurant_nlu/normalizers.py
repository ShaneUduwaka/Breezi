
from __future__ import annotations

import re
from typing import Optional

from .patterns import SLOT_SYNONYMS


NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "එකක්": 1,
    "දෙකක්": 2,
    "තුනක්": 3,
    "හතරක්": 4,
    "පහක්": 5,
}


def normalize_slot_value(slot_name: str, value: str) -> str:
    raw = value.strip()
    lowered = raw.lower()

    if slot_name in SLOT_SYNONYMS and lowered in SLOT_SYNONYMS[slot_name]:
        return SLOT_SYNONYMS[slot_name][lowered]

    if slot_name in {"quantity", "points", "headcount"}:
        normalized = normalize_number(raw)
        return str(normalized) if normalized is not None else raw

    if slot_name == "phone_number":
        digits = re.sub(r"\D", "", raw)
        if digits.startswith("94") and len(digits) == 11:
            return f"+{digits}"
        if digits.startswith("0") and len(digits) == 10:
            return digits
        return raw

    if slot_name in {"amount"}:
        m = re.search(r"(\d+(?:[.,]\d{2})?)", raw)
        return m.group(1).replace(",", "") if m else raw

    return raw


def normalize_number(text: str) -> Optional[int]:
    candidate = text.strip().lower()
    if candidate.isdigit():
        return int(candidate)
    if candidate in NUMBER_WORDS:
        return NUMBER_WORDS[candidate]
    m = re.search(r"\d+", candidate)
    if m:
        return int(m.group())
    return None
