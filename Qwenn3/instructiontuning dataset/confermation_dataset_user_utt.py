import os
import json
import random
import hashlib
import time
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
from openai import OpenAI

# ----------------------------
# OpenAI client
# ----------------------------
load_dotenv(dotenv_path=".env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-5-mini"

def llm_text(prompt: str, *, max_retries: int = 3) -> str:
    last_err = None
    for attempt in range(max_retries):
        try:
            resp = client.responses.create(
                model=MODEL,
                input=prompt,
            )
            text = (resp.output_text or "").strip()
            if not text:
                raise RuntimeError("Empty output_text")
            return text
        except Exception as e:
            last_err = e
            time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"LLM call failed after retries: {last_err}")

# ----------------------------
# Scenario pools
# ----------------------------
CALLER_TYPES = [
    "student", "office worker", "parent ordering for family", "driver",
    "elderly caller", "young couple", "tourist"
]

VARIATIONS = [
    "Sinhala-heavy, polite, short",
    "Balanced Sinhala/Singlish, natural",
    "Singlish-heavy, slightly rushed"
]

CONTEXTS = [
    "calling from a bus",
    "calling during lunch break",
    "calling while driving (hands-free)",
    "calling during heavy rain",
    "planning dinner with friends",
    "ordering late night food"
]

STYLES = ["Direct", "Vague & Rambling", "Frustrated", "Polite", "Rushed", "Confused"]

INTENTS = [
    "order_delivery",
    "order_takeaway",
    "dinein_reservation",
    "menu_inquiry",
    "order_modification",
    "complaint",
    "opening_hours",
    "cancel_order",
]

SLOT_SCHEMA: Dict[str, List[str]] = {
    "order_delivery": ["food_item", "quantity", "delivery_address", "phone_number", "payment_method"],
    "order_takeaway": ["food_item", "quantity", "pickup_time", "name", "phone_number"],
    "dinein_reservation": ["reservation_date", "reservation_time", "table_size", "name", "phone_number"],
    "menu_inquiry": ["question_topic"],
    "order_modification": ["order_id", "change_request"],
    "complaint": ["order_id", "issue"],
    "opening_hours": ["day_or_date"],
    "cancel_order": ["order_id", "reason"],
}

AUDIT_CATEGORIES = [
    "delivery fee",
    "ETA",
    "pickup readiness",
    "reservation hold policy",
    "cancellation policy",
    "promo condition",
    "substitution availability",
    "allergy or spice handling"
]

LAST_MINUTE_CHANGES = [
    "address",
    "time",
    "quantity",
    "payment method",
    "item",
    "spice level",
    "none"
]

FOOD_ITEMS = [
    "චිකන් කොත්තු", "ෆ්‍රයිඩ් රයිස්", "බිර්යනි", "හොප්පර්ස්", "ස්ට්‍රිං හොප්පර්ස්", "බර්ගර්"
]
AREAS = ["නුගේගොඩ", "දෙහිවල", "මහරගම", "රාජගිරිය", "කොල්ලුපිටිය"]
NAMES = ["නිමල්", "කාසුන්", "සචිනි", "පියුමි", "දිල්ශාන්", "තිලිනි"]

def scenario_signature(s: dict) -> str:
    blob = json.dumps(s, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()

def sample_slot_value(slot_name: str) -> str:
    if slot_name == "food_item":
        return random.choice(FOOD_ITEMS)
    elif slot_name == "quantity":
        return str(random.randint(1, 5))
    elif slot_name == "delivery_address":
        return random.choice(AREAS)
    elif slot_name == "phone_number":
        return "07" + "".join(str(random.randint(0, 9)) for _ in range(8))
    elif slot_name == "payment_method":
        return random.choice(["cash", "card", "online"])
    elif slot_name == "pickup_time":
        return random.choice(["7.00", "7.30", "8.00", "8.30"])
    elif slot_name == "name":
        return random.choice(NAMES)
    elif slot_name == "reservation_date":
        return random.choice(["අද", "හෙට", "සෙනසුරාදා", "ඉරිදා"])
    elif slot_name == "reservation_time":
        return random.choice(["7.00", "7.30", "8.00"])
    elif slot_name == "table_size":
        return str(random.randint(2, 8))
    elif slot_name == "question_topic":
        return random.choice(["menu", "price", "availability"])
    elif slot_name == "order_id":
        return str(random.randint(10000, 99999))
    elif slot_name == "change_request":
        return random.choice(["spicy අඩු කරන්න", "onion අයින් කරන්න", "time එක වෙනස් කරන්න"])
    elif slot_name == "issue":
        return random.choice(["late", "wrong item", "cold food"])
    elif slot_name == "day_or_date":
        return random.choice(["අද", "හෙට", "සෙනසුරාදා"])
    elif slot_name == "reason":
        return random.choice(["plans changed", "late", "වෙන තැනකින් ගත්තා"])
    return f"sample_{slot_name}"

def build_state4_slots(intent: str) -> Tuple[dict, list]:
    required = SLOT_SCHEMA.get(intent, [])
    filled_slots = {}

    for slot in required:
        filled_slots[slot] = sample_slot_value(slot)

    if required and random.random() < 0.25:
        missing_slot = random.choice(required)
        filled_slots.pop(missing_slot, None)
        missing_slots = [missing_slot]
    else:
        missing_slots = []

    return filled_slots, missing_slots

def prompt_user_utterance_state4(state_name: str, scenario: dict, filled_slots: dict, missing_slots: List[str]) -> str:
    return f"""
You are generating ONLY the caller's spoken words for a Sri Lankan restaurant phone call.

STATE: {state_name}

Background scenario (for tone only):
Caller type: {scenario["caller_type"]}
Situation: {scenario["context"]}
Speaking style: {scenario["style"]}
Variation: {scenario["variation"]}

Underlying intent (do NOT output this label): {scenario["intent"]}

Known details already confirmed:
{json.dumps(filled_slots, ensure_ascii=False)}

Still missing:
{json.dumps(missing_slots, ensure_ascii=False)}

Audit concern for this row:
{scenario["audit_category"]}

Possible final change for this row:
{scenario["last_minute_change"]}

The scenario information above is background only.
Do NOT describe it directly in the caller's speech.

Speech style:
Use natural spoken Sinhala used in everyday Sri Lankan phone calls.
Prefer spoken Sinhala sentence structure.
Use English words only when commonly used in local speech, such as order, pickup, delivery, number, time.
Avoid translated English phrasing.
Avoid formal written Sinhala.
Avoid robotic wording.
Keep the speech casual, brief, and realistic.

Conversation requirements:
- The caller is near the end of the conversation.
- Most details are already confirmed.
- The caller should either:
  1) confirm the request,
  2) ask one realistic audit question,
  3) or raise one last-minute change.
- Naturally refer to already known details if needed.
- Do not mention intent labels.

Output rules:
- One utterance only
- 1–3 short sentences
- No lists
- No explanations or metadata
- Output ONLY the caller's spoken words
""".strip()

def build_state4_user_row(row_index: int, used_sigs: set) -> Optional[dict]:
    intent = random.choice(INTENTS)
    filled_slots, missing_slots = build_state4_slots(intent)

    scenario = {
        "intent": intent,
        "caller_type": random.choice(CALLER_TYPES),
        "context": random.choice(CONTEXTS),
        "style": random.choice(STYLES),
        "variation": random.choice(VARIATIONS),
        "state": "State 4: Confirmation & Audit",
        "audit_category": random.choice(AUDIT_CATEGORIES),
        "last_minute_change": random.choice(LAST_MINUTE_CHANGES),
    }

    sig = scenario_signature({
        **scenario,
        "filled_slots": filled_slots,
        "missing_slots": missing_slots,
    })
    if sig in used_sigs:
        return None
    used_sigs.add(sig)

    user_utt = llm_text(
        prompt_user_utterance_state4(
            "State 4: Confirmation & Audit",
            scenario,
            filled_slots,
            missing_slots
        )
    )

    instruction = "You are a Breezi Sinhala Call Agent. Handle final confirmation, audit concerns, and last-minute changes naturally."
    context_memory = "Near resolution. Most details already confirmed. Final confirmation stage."

    return {
        "instruction": instruction,
        "input": {
            "current_state": "State 4: Confirmation & Audit",
            "intent": intent,
            "filled_slots": filled_slots,
            "missing_slots": missing_slots,
            "user_utterance": user_utt,
            "context_memory": context_memory,
        },
        "output": ""
    }

def generate_state4_user_jsonl(path: str, total_rows: int = 20):
    used_sigs = set()
    rows_written = 0

    with open(path, "w", encoding="utf-8") as f:
        while rows_written < total_rows:
            row = build_state4_user_row(rows_written + 1, used_sigs)
            if row is None:
                continue
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            rows_written += 1

    print(f"Wrote {rows_written} rows to {path}")

if __name__ == "__main__":
    generate_state4_user_jsonl("state4_user_rows.jsonl", total_rows=20)