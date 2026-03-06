import os
import json
import random
import hashlib
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

from openai import OpenAI  # pip install openai

# ----------------------------
# OpenAI client
# ----------------------------
client = OpenAI()  # reads OPENAI_API_KEY from env :contentReference[oaicite:2]{index=2}

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
CALLER_TYPES = []

VARIATIONS = []

CONTEXTS = []

STYLES = []

INTENTS = [
]




def scenario_signature(s: dict) -> str:
    """Dedup based on scenario structure (not exact text)."""
    blob = json.dumps(s, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def prompt_user_utterance_state2(state_name: str, scenario: dict) -> str:
    """
    State 2: Intent discovery user utterance.
    Must clearly hint/express intent WITHOUT labels; minimal info; sometimes ambiguous.
    """
    return f"""
You are generating ONLY the caller's spoken words for a Sri Lankan restaurant phone call.

STATE: {state_name}
Line status: greeting finished, line clear.
Caller type: {scenario["caller_type"]}
Situation: {scenario["context"]}
Speaking style: {scenario["style"]}
Variation: {scenario["variation"]}

Underlying intent (do NOT output this label): {scenario["intent"]}

Rules:
- The caller MUST clearly hint/express the intent naturally (do NOT name any intent labels).
- caller must provide MINIMAL info (0-2 details).

Constraints:
- Language: Sinhala with natural Singlish (Sri Lanka).
- Sound like real phone speech.
- 1-2 sentences preferred (max 3).
- No metadata, no explanations. Output ONLY the caller's speech.
- Create plausible values if visible slots exist.
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


def prompt_agent_response_state2(scenario: dict, user_utterance: str) -> str:
    """
    State 2 agent response: confirm/clarify intent + ask 1-3 best questions.
    We keep the same mandatory think format.
    """
    return f"""
You are a professional Sri Lankan restaurant phone-call assistant.

STATE: State 2: Intent Discovery
Caller said:
\"\"\"{user_utterance}\"\"\"

Hard rules:
- Respond in Sinhala with natural Singlish where appropriate. .
- Do NOT mention intent labels like "{scenario["intent"]}".
- Do NOT invent facts not stated by the caller.
- First, reflect what you THINK they want in normal words (e.g., delivery / takeaway / reservation / hours / complaint).
- Ask ONLY 1-3 questions total.
- Your questions should either confirm the request if ambiguous OR collect the most important missing details.

OUTPUT FORMAT (MANDATORY):
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
        "context": random.choice(CONTEXTS),
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
            

            if row is None:
                continue

            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            rows_written += 1

    print(f"Wrote {rows_written} rows to {path}")


if __name__ == "__main__":
    generate_jsonl("restaurant_state2_state3_2000.jsonl", total_rows=2000, state2_ratio=0.5)