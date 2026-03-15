import os
import json
import random
import hashlib
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from dotenv import load_dotenv
from openai import OpenAI  # pip install openai

# ----------------------------
# OpenAI client
# ----------------------------
load_dotenv(dotenv_path=".env") # Load environment variables from .env file
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-5-mini"  # pick the model you want available in your account

def llm_text(prompt: str, *, max_retries: int = 3) -> str:
    """Simple non-streaming call; retries on transient errors."""
    last_err = None
    for attempt in range(max_retries):
        try:
            resp = client.responses.create(
                model=MODEL,
                input=prompt,
            )
            text = (resp.output_text or "").strip()
            if not text:
                # Sometimes output_text can be empty in edge cases; treat as retryable. :contentReference[oaicite:3]{index=3}
                raise RuntimeError("Empty output_text")
            return text
        except Exception as e:
            last_err = e
            time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"LLM call failed after retries: {last_err}")

# ----------------------------
# Scenario pools (small, not huge)
# ----------------------------
CALLER_TYPES = [
    "student", "office worker", "parent ordering for family", "driver", "elderly caller",
    "young couple", "tourist"]

VARIATIONS = ["Sinhala-heavy, polite, short",
              "Balanced Sinhala/Singlish, natural",
              "Singlish-heavy, slightly rushed"]

CONTEXTS = [
    "calling from a bus", "calling during lunch break", "calling while driving (hands-free)",
    "calling during heavy rain", "planning dinner with friends", "ordering late night food"]

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

def pick_visible_missing(intent: str) -> Tuple[List[str], List[str]]:
    required = SLOT_SCHEMA.get(intent, [])
    if not required:
        return [], []
    # show 2–4 slots if possible, leave 1–3 missing
    k = min(len(required), random.randint(2, max(2, min(4, len(required)))))
    visible = random.sample(required, k=k)
    missing = [s for s in required if s not in visible]
    # ensure at least 1 missing for slot-filling intents
    if len(required) > 1 and not missing:
        missing = [visible.pop()]
    return visible, missing

def scenario_signature(s: dict) -> str:
    """Dedup based on scenario structure (not exact text)."""
    blob = json.dumps(s, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()

# ----------------------------
# Prompts
# ----------------------------
def prompt_user_utterance(state_name: str, scenario: dict, visible_slots: List[str], missing_slots: List[str]) -> str:
    # State 3 (slot filling user turn): user provides some info, omits others
    # We keep it as a single utterance to match your row format.
    return f"""
You are generating ONLY the caller's spoken words for a Sri Lankan restaurant phone call.

STATE: {state_name}

Background scenario (for tone only):
Caller type: {scenario["caller_type"]}
Speaking style: {scenario["style"]}
Variation: {scenario["variation"]}

Underlying intent (do NOT output this label): {scenario["intent"]}

The scenario information above is background context only.
Do NOT repeat or describe the scenario directly in the caller’s speech.
Use it only to influence tone and make up a real life call scenario.

Speech style:
Use natural spoken Sinhala typical of everyday Sri Lankan phone calls.
Prefer Sinhala sentence structure and only use English words common in local speech (order, pickup, delivery).
Avoid translated English phrasing or formal business language.
Keep the speech casual, brief, and conversational with short phone-style sentences.

Conversation requirements:

Naturally include details corresponding to these slot types:
{visible_slots}

The caller MUST NOT mention details corresponding to these slot types:
{missing_slots}

Output rules:

- One utterance only
- 1-3 sentences
- No explanations or metadata
- Output ONLY the caller's spoken words
""".strip()

def prompt_user_utterance_state2(state_name: str, scenario: dict) -> str:
    """
    State 2: Intent discovery user utterance.
    Must clearly hint/express intent WITHOUT labels; minimal info; sometimes ambiguous.
    """
    return f"""
You are generating ONLY the caller's spoken words for a Sri Lankan restaurant phone call.

STATE: {state_name}
Line status: greeting finished, line clear.

Background scenario (for tone only):
Caller type: {scenario["caller_type"]}
Speaking style: {scenario["style"]}
Variation: {scenario["variation"]}

Underlying intent (do NOT output this label): {scenario["intent"]}

The scenario information above is background context only.
Do NOT describe the scenario directly in the caller's speech.
Use it only to influence tone and make up a real life call scenario.

Speech style:
Use natural spoken Sinhala typical of everyday Sri Lankan phone calls.
Prefer Sinhala sentence structure and only use English words common in local speech (order, pickup, delivery).
Avoid translated English phrasing, robotic wording and formal business language.
Keep the speech casual and brief with short conversational sentences.

Conversation rules:

- The caller should clearly hint at their request naturally without naming any intent labels.
- Provide minimal information (0-2 small details only).

Output rules:

- One short utterance
- 1-2 sentences (max 3)
- No explanations or metadata
- Output ONLY the caller's spoken words
""".strip()

def prompt_extract_slots(intent: str, user_utterance: str) -> str:
    # This lets the model propose filled slots present in the utterance.
    # Missing slots can be computed from schema; we still ask for both for consistency.
    schema = SLOT_SCHEMA.get(intent, [])
    return f"""
Extract slots for a restaurant call.

Underlying intent (hidden label): {intent}
Slot schema for this intent: {schema}

Caller utterance:
\"\"\"{user_utterance}\"\"\"

Return STRICT JSON only with keys:
- "filled_slots": object (only what is explicitly stated; do not guess)
- "missing_slots": array (slot names from schema that are not in filled_slots)

Rules:
- Do not add extra keys.
- Do not hallucinate values.
""".strip()

def prompt_agent_response(state_name: str, scenario: dict, user_utterance: str, filled_slots: dict, missing_slots: List[str]) -> str:
    return f"""
You are a Sri Lankan restaurant phone-call assistant speaking to a caller.

STATE: {state_name}

Caller said:
\"\"\"{user_utterance}\"\"\"

Known details (filled_slots):
{json.dumps(filled_slots, ensure_ascii=False)}

Missing details needed to complete the request:
{json.dumps(missing_slots, ensure_ascii=False)}
Speech style:
Use natural spoken Sinhala typical of everyday Sri Lankan restaurant phone calls.
Keep the tone polite, respectful, customer-friendly, and conversational.
Prefer polite forms of address such as "oba thuma", "mahattaya", "miss", or other natural respectful wording when appropriate.
Prefer Sinhala sentence structure and use English words only when they are commonly used in local speech (order, pickup, delivery).
Avoid translated English phrasing, robotic wording, or harsh language.
Keep the response clear, warm, and professional while still sounding natural.

Rules:

- Do NOT mention intent labels like "{scenario["intent"]}".
- Do NOT invent facts not stated by the caller.
- Use filled_slots as known details.
- Answer the caller first, then ask 1-3 short questions for missing_slots if needed.
- Avoid repeating the caller's words.
- If nothing is missing, give a helpful final response.

Output format (MANDATORY):

<think>SHORT PLAN (<=20 words). Checklist only. No step-by-step reasoning.</think>
Then the final agent response text (no extra tags).
""".strip()

def prompt_agent_response_state2(scenario: dict, user_utterance: str) -> str:
    """
    State 2 agent response: confirm/clarify intent + ask 1-3 best questions.
    We keep the same mandatory think format.
    """
    return f"""
You are a Sri Lankan restaurant phone-call assistant speaking to a caller.

STATE: State 2 — Intent Discovery

Caller said:
\"\"\"{user_utterance}\"\"\"

Speech style:
Use natural spoken Sinhala typical of everyday Sri Lankan restaurant phone calls.
Keep the tone polite, respectful, customer-friendly, and conversational.
Prefer polite forms of address such as "oba thuma", "mahattaya", "miss", or other natural respectful wording when appropriate.
Prefer Sinhala sentence structure and use English words only when they are commonly used in local speech (order, pickup, delivery).
Avoid translated English phrasing, robotic wording, or harsh language.
Keep the response clear, warm, and professional while still sounding natural.

Rules:

- Do NOT mention intent labels like "{scenario["intent"]}".
- Do NOT invent facts not stated by the caller.
- Use filled_slots as known details.
- Answer the caller first, then ask 1-3 short questions for missing_slots if needed.
- Avoid repeating the caller's words.
- If nothing is missing, give a helpful final response.

Output format (MANDATORY):

<think>SHORT PLAN (<=20 words). Checklist only. No step-by-step reasoning.</think>
Then the final agent response text (no extra tags).
""".strip()



# ----------------------------
# One row generator (State 3 example)
# ----------------------------

def build_state2_row(row_index: int, used_sigs: set) -> Optional[dict]:
    intent = random.choice(INTENTS)

    scenario = {
        "intent": intent,
        "caller_type": random.choice(CALLER_TYPES),
        "style": random.choice(STYLES),
        "variation": random.choice(VARIATIONS),
        "state": "State 2: Intent Discovery",
        "visible_slots": "-",
        "missing_slots": "-",
    }

    sig = scenario_signature(scenario)
    if sig in used_sigs:
        return None
    used_sigs.add(sig)

    # 1) Generate user utterance (intent hinted, minimal info)
    user_utt = llm_text(prompt_user_utterance_state2("State 2: Intent Discovery", scenario))

    # 2) Optional slot extraction (works even if empty); safe fallback
    slots_json = llm_text(prompt_extract_slots(intent, user_utt))
    try:
        slots = json.loads(slots_json)
        filled_slots = slots["filled_slots"]
        missing_slots = slots["missing_slots"]
        if not isinstance(filled_slots, dict) or not isinstance(missing_slots, list):
            raise ValueError("Bad types")
    except Exception:
        filled_slots = {}
        missing_slots = SLOT_SCHEMA.get(intent, [])

    # 3) Generate agent response (confirm intent + ask 1–3 questions)
    agent_out = llm_text(prompt_agent_response_state2(scenario, user_utt))

    instruction = "You are a Breezi Sinhala Call Agent. Identify the caller’s request and ask 1–3 clarifying questions."
    context_memory = "Call answered and greeted. Line clear. Start intent discovery."

    return {
        "instruction": instruction,
        "input": {
            "current_state": "State 2: Intent Discovery",
            "intent": intent,                # label stored for training, but NOT spoken in text
            "filled_slots": filled_slots,    # may be empty
            "missing_slots": missing_slots,
            "user_utterance": user_utt,
            "context_memory": context_memory,
        },
        "output": agent_out
    }

def build_state3_row(row_index: int, used_sigs: set) -> Optional[dict]:
    intent = random.choice(INTENTS)
    visible, missing = pick_visible_missing(intent)

    scenario = {
        "intent": intent,
        "caller_type": random.choice(CALLER_TYPES),
        "style": random.choice(STYLES),
        "variation": random.choice(VARIATIONS),
        "state": "State 3: Slot Filling",
        "visible_slots": visible,
        "missing_slots": missing,
    }

    sig = scenario_signature(scenario)
    if sig in used_sigs:
        return None
    used_sigs.add(sig)

    # 1) Generate user utterance
    user_utt = llm_text(prompt_user_utterance("State 3: Slot Filling", scenario, visible, missing))

    # 2) Extract slots (filled + missing) from utterance
    slots_json = llm_text(prompt_extract_slots(intent, user_utt))
    try:
        slots = json.loads(slots_json)
        filled_slots = slots["filled_slots"]
        missing_slots = slots["missing_slots"]
        if not isinstance(filled_slots, dict) or not isinstance(missing_slots, list):
            raise ValueError("Bad types")
    except Exception:
        # If parse fails, fall back to schema-based missing
        filled_slots = {}
        missing_slots = SLOT_SCHEMA.get(intent, [])

    # 3) Generate agent response (<think> + response)
    agent_out = llm_text(prompt_agent_response("State 3: Slot Filling", scenario, user_utt, filled_slots, missing_slots))

    # 4) Build row in your schema
    instruction = "You are a Breezi Sinhala Call Agent. Ask targeted questions to fill missing details."
    context_memory = f"Restaurant call. Caller type: {scenario['caller_type']}. Style: {scenario['style']}."

    return {
        "instruction": instruction,
        "input": {
            "current_state": "State 3: Slot Filling",
            "intent": intent,
            "filled_slots": filled_slots,
            "missing_slots": missing_slots,
            "user_utterance": user_utt,
            "context_memory": context_memory,
        },
        "output": agent_out
    }

# ----------------------------
# Main: generate N rows and save JSONL
# ----------------------------
def generate_jsonl(path: str, total_rows: int = 2000, state2_ratio: float = 0.5):
    """
    state2_ratio=0.5 means ~50% State 2 rows, ~50% State 3 rows.
    Adjust as needed.
    """
    used_sigs = set()
    rows_written = 0

    with open(path, "w", encoding="utf-8") as f:
        while rows_written < total_rows:
            # choose state 2 or state 3
            do_state2 = (random.random() < state2_ratio)

            if do_state2:
                row = build_state2_row(rows_written + 1, used_sigs)
            else:
                row = build_state3_row(rows_written + 1, used_sigs)

            if row is None:
                continue

            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            rows_written += 1

    print(f"Wrote {rows_written} rows to {path}")


if __name__ == "__main__":
    generate_jsonl("restaurant_test_2000.jsonl", total_rows=2000, state2_ratio=0.5)