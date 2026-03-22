import os
import json
import random
import hashlib
import time
from typing import Dict, List, Tuple, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ----------------------------
# Gemini client
# ----------------------------
# Load .env from current directory or script directory
env_path = os.path.join(os.path.dirname(__file__), ".env")
if not os.path.exists(env_path):
    env_path = ".env"  # Fallback to current working directory
load_dotenv(dotenv_path=env_path, verbose=True)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment")
client = genai.Client(api_key=api_key)

# Best match for a fast text model in current Gemini API
MODEL = "gemini-3.1-flash-lite-preview"


def llm_text(prompt: str, *, max_retries: int = 3) -> str:
    """Simple non-streaming call with basic retry logic."""
    last_err = None
    for attempt in range(max_retries):
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                ),
            )
            text = (resp.text or "").strip()
            if not text:
                raise RuntimeError("Empty response text")
            return text
        except Exception as e:
            last_err = e
            time.sleep(0.8 * (attempt + 1))
    raise RuntimeError(f"LLM call failed after retries: {last_err}")


# ----------------------------
# Scenario pools
# ----------------------------
CALLER_TYPES = [
    "student",
    "office worker",
    "parent ordering for family",
    "driver",
    "elderly caller",
    "young adult",
    "regular customer",
]

VARIATIONS = [
    "native urban Sinhala phrasing",
    "native semi-urban Sinhala phrasing",
    "native rural Sinhala phrasing",
    "native educated Sinhala phrasing",
    "native casual everyday Sinhala phrasing",
]

CONTEXTS = [
    "in a hurry",
    "ordering for self",
    "ordering for family",
    "ordering for a small group",
    "not sure what to order",
    "already knows what they want",
    "checking before ordering",
    "following up on an existing order",
    "calling close to meal time",
    "calling late in the evening",
    "trying to keep it simple",
    "concerned about timing",
]

STYLES = [
    "Direct",
    "Slightly vague",
    "Frustrated",
    "Polite",
    "Rushed",
    "Confused",
]

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
    "order_delivery": [
        "food_item",
        "quantity",
        "delivery_address",
        "landmark",
        "phone_number",
        "payment_method",
        "special_request",
        "spice_level",
    ],
    "order_takeaway": [
        "food_item",
        "quantity",
        "pickup_time",
        "name",
        "phone_number",
        "special_request",
    ],
    "dinein_reservation": [
        "reservation_date",
        "reservation_time",
        "table_size",
        "name",
        "phone_number",
        "special_request",
    ],
    "menu_inquiry": [
        "food_item",
        "category",
        "price_range",
        "availability",
        "question_topic",
    ],
    "order_modification": [
        "order_id",
        "food_item",
        "change_request",
        "quantity",
    ],
    "complaint": [
        "order_id",
        "issue",
        "food_item",
        "severity",
        "requested_resolution",
    ],
    "opening_hours": [
        "day_or_date",
        "time_range",
        "meal_type",
    ],
    "cancel_order": [
        "order_id",
        "reason",
        "urgency",
    ],
}

PRIORITY_SLOTS: Dict[str, List[str]] = {
    "order_delivery": ["food_item"],
    "order_takeaway": ["food_item"],
    "dinein_reservation": ["reservation_date", "reservation_time"],
    "menu_inquiry": ["question_topic"],
    "order_modification": ["order_id", "change_request"],
    "complaint": ["order_id", "issue"],
    "opening_hours": ["day_or_date"],
    "cancel_order": ["order_id"],
}

PREFER_MISSING: Dict[str, List[str]] = {
    "order_delivery": ["landmark", "payment_method", "special_request", "spice_level"],
    "order_takeaway": ["pickup_time", "special_request"],
    "dinein_reservation": ["special_request", "phone_number"],
    "menu_inquiry": ["price_range", "availability"],
    "order_modification": ["quantity"],
    "complaint": ["severity", "requested_resolution"],
    "opening_hours": ["meal_type", "time_range"],
    "cancel_order": ["urgency", "reason"],
}

SLOT_VALUE_POOLS: Dict[str, List[str]] = {
    "food_item": [
        "චිකන් කොත්තු",
        "චීස් කොත්තු",
        "එග් ෆ්‍රයිඩ් රයිස්",
        "චිකන් ෆ්‍රයිඩ් රයිස්",
        "චිකන් බර්ගර්",
        "වෙජිටබල් නූඩ්ල්ස්",
        "චිකන් නූඩ්ල්ස්",
        "නාසි ගොරෙන්",
        "බිරියානි එකක්",
    ],
    "quantity": [
        "එකක්",
        "දෙකක්",
        "තුනක්",
        "හතරක්",
    ],
    "delivery_address": [
        "නුගේගොඩට",
        "මහරගමට",
        "කොට්ටාවට",
        "බත්තරමුල්ලට",
        "පන්නිපිටියට",
        "මාලබේට",
    ],
    "landmark": [
        "පන්සල ළඟ",
        "පාසල ඉස්සරහ",
        "බස් හෝල්ට් එක ළඟ",
        "පෙට්‍රල් ෂෙඩ් එක ළඟ",
        "බැංකුව පහුකරලා",
    ],
    "phone_number": [
        "0712345678",
        "0771234567",
        "0759988776",
        "0704455667",
    ],
    "payment_method": [
        "කෑෂ් වලින්",
        "කාඩ් එකෙන්",
    ],
    "special_request": [
        "ටිකක් අඩු සැරට",
        "ලූනු නැතුව",
        "extra gravy එක්ක",
        "මිරිස් අඩුවෙන්",
        "egg එකක් අමතරව",
    ],
    "spice_level": [
        "සැර අඩුවෙන්",
        "මැද සැරට",
        "හොඳට සැරට",
    ],
    "pickup_time": [
        "හයයි තිහට",
        "හතට",
        "හතයි කාලට",
        "රෑ අටට",
    ],
    "name": [
        "කසුන්",
        "නිමාලි",
        "චතුරි",
        "දිනේෂ්",
        "හංසිකා",
    ],
    "reservation_date": [
        "අද",
        "හෙට",
        "අනිද්දා",
        "සෙනසුරාදා",
        "ඉරිදා",
    ],
    "reservation_time": [
        "දවල් දොළහට",
        "හවස හයට",
        "රෑ හතට",
        "රෑ අටට",
    ],
    "table_size": [
        "දෙන්නෙක්ට",
        "හතර දෙනෙක්ට",
        "හය දෙනෙක්ට",
        "අට දෙනෙක්ට",
    ],
    "category": [
        "කොත්තු",
        "fried rice",
        "noodles",
        "veg items",
        "seafood items",
    ],
    "price_range": [
        "1000ට අඩු",
        "1500ට වගේ",
        "2000ට ඇතුළත",
    ],
    "availability": [
        "තියෙනවද",
        "අද available ද",
    ],
    "question_topic": [
        "menu එක",
        "prices",
        "veg options",
        "today specials",
        "delivery charges",
    ],
    "order_id": [
        "12345",
        "5689",
        "A102",
        "B447",
    ],
    "change_request": [
        "quantity එක දෙකක් කරන්න",
        "address එක වෙනස් කරන්න",
        "item එක මාරු කරන්න",
        "pickup time එක ටිකක් පස්සට දාන්න",
    ],
    "issue": [
        "order එක පරක්කුයි",
        "food එක තණ්ඩි වෙලා",
        "වැරදි item එක ඇවිල්ලා",
        "quantity එක අඩුයි",
    ],
    "severity": [
        "ටිකක්",
        "ගොඩක්",
        "හොඳටම",
    ],
    "requested_resolution": [
        "replace කරලා දෙන්න",
        "refund එකක් දෙන්න",
        "ආයෙ හරි order එක යවන්න",
    ],
    "day_or_date": [
        "අද",
        "හෙට",
        "ඉරිදා",
        "සෙනසුරාදා",
    ],
    "time_range": [
        "උදේ",
        "දවල්ට",
        "හවසට",
        "රෑට",
    ],
    "meal_type": [
        "breakfast",
        "lunch",
        "dinner",
    ],
    "reason": [
        "දැන් ඕනෙ නැහැ",
        "late වෙන නිසා",
        "plan එක වෙනස් වුණා",
        "වැරදිවෙලා දාගත්තෙ",
    ],
    "urgency": [
        "දැන්ම",
        "ඉක්මනට",
        "පුළුවන් තරම් ඉක්මනට",
    ],
}


# ----------------------------
# Helpers
# ----------------------------
def scenario_signature(s: dict) -> str:
    """Dedup based on scenario structure (not exact text)."""
    blob = json.dumps(s, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def safe_json_loads(text: str) -> Optional[dict]:
    """Parse JSON robustly; tolerate fenced blocks."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        return json.loads(text)
    except Exception:
        return None


def pick_visible_missing(intent: str) -> Tuple[List[str], List[str]]:
    """Choose visible and missing slots for State 3."""
    required = SLOT_SCHEMA.get(intent, [])
    if not required:
        return [], []

    priority = PRIORITY_SLOTS.get(intent, [])
    prefer_missing = set(PREFER_MISSING.get(intent, []))

    visible: List[str] = []

    if priority:
        visible.append(random.choice(priority))

    remaining = [s for s in required if s not in visible]

    target_visible_count = random.randint(
        1 if len(required) <= 2 else 2,
        min(4, len(required)),
    )

    non_prefer_missing = [s for s in remaining if s not in prefer_missing]
    random.shuffle(non_prefer_missing)
    random.shuffle(remaining)

    while len(visible) < target_visible_count and non_prefer_missing:
        visible.append(non_prefer_missing.pop())

    while len(visible) < target_visible_count and remaining:
        slot = remaining.pop()
        if slot not in visible:
            visible.append(slot)

    visible = list(dict.fromkeys(visible))
    missing = [s for s in required if s not in visible]

    if len(required) > 1 and not missing:
        moved = visible.pop()
        missing = [moved]

    return visible, missing


def sample_slot_values(intent: str, visible_slots: List[str]) -> Dict[str, str]:
    """Generate concrete slot values for the visible slots."""
    values: Dict[str, str] = {}
    for slot in visible_slots:
        pool = SLOT_VALUE_POOLS.get(slot)
        if pool:
            values[slot] = random.choice(pool)
        else:
            values[slot] = f"{slot}_value"
    return values


def validate_scenario(scenario: dict) -> bool:
    """Reject obviously odd combinations."""
    caller_type = scenario["caller_type"]
    context = scenario["context"]
    intent = scenario["intent"]

    if caller_type == "elderly caller" and scenario["style"] == "Rushed":
        return False
    if caller_type == "driver" and context == "ordering for family":
        return False
    if intent == "dinein_reservation" and context == "following up on an existing order":
        return False
    if intent == "opening_hours" and context == "ordering for a small group":
        return False
    if intent == "complaint" and context == "already knows what they want":
        return False
    return True


# ----------------------------
# Prompts
# ----------------------------
def prompt_user_utterance_state2(state_name: str, scenario: dict) -> str:
    return f"""
Generate ONLY the caller's spoken words for a Sri Lankan restaurant phone call.

STATE: {state_name}
Line status: greeting finished, line clear.

Background context (do NOT output):
Caller: {scenario["caller_type"]}
Context: {scenario["context"]}
Style: {scenario["style"]}
Variation: {scenario["variation"]}
Intent: {scenario["intent"]}

Use this as hidden background to simulate a real caller. Do NOT describe it directly; reflect it only through natural tone, wording, urgency, politeness, hesitation, or phrasing.

Language:
Use natural spoken Sinhala in Sinhala script (සිංහල) only.
Do NOT write Sinhala in English letters or produce Singlish.
Always follow correct Sinhala grammar and sentence structure.
English words may be used only if commonly embedded in Sri Lankan speech (e.g., order, pickup, delivery), and must be minimal and within Sinhala sentence structure.
Avoid English-dominant or translated phrasing.

Conversation rules:
- The utterance must match the purpose of the STATE and clearly imply the caller’s request.
- Include only what a real caller would naturally say at this point in the call—usually 0–2 small relevant details only if natural.
- Do NOT force details.
- Keep it casual, brief, and conversational.

Output rules:
- One short utterance
- 1–2 sentences (max 3)
- No explanations or metadata
- Output ONLY the caller's spoken words
""".strip()


def prompt_user_utterance_state3(
    state_name: str,
    scenario: dict,
    filled_slots: Dict[str, str],
    missing_slots: List[str],
) -> str:
    return f"""
Generate ONLY the caller’s spoken words for a Sri Lankan restaurant phone call.

STATE: {state_name}

Background context (do NOT output):
Caller: {scenario["caller_type"]}
Context: {scenario["context"]}
Style: {scenario["style"]}
Variation: {scenario["variation"]}
Intent: {scenario["intent"]}

Use this as hidden background to simulate a real caller. Do NOT describe it directly; reflect it only through natural tone, wording, urgency, politeness, hesitation, or phrasing.

Language:
Use fluent, natural spoken Sinhala in Sinhala script (සිංහල) only.
Do NOT write Sinhala in English letters or produce Singlish.
Always follow correct Sinhala grammar and sentence structure.
English words may be used only if commonly embedded (e.g., order, pickup, delivery), and must be minimal and within Sinhala structure.
Avoid English-dominant or translated phrasing.

Behavior:
Caller may ask, request, order, confirm, or clarify naturally. Keep it casual, brief, and conversational. Allow natural fillers when appropriate. Avoid overly formal or structured phrasing.

Known details the caller may naturally mention:
{json.dumps(filled_slots, ensure_ascii=False)}

Do NOT mention or imply these missing slot types:
{json.dumps(missing_slots, ensure_ascii=False)}

Rules:
- The utterance must naturally include the known details above.
- Do NOT list or enumerate them mechanically.
- Do NOT invent any extra details.
- Do NOT generate values for missing slots.
- Prioritize natural conversational flow over mentioning everything.

Output:
- One utterance only
- 1–3 short sentences
- ONLY caller speech
- No explanations or metadata
""".strip()


def prompt_extract_slots(intent: str, user_utterance: str) -> str:
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
- Use only information explicitly stated in the utterance.
""".strip()


def prompt_agent_response_state2(
    scenario: dict,
    user_utterance: str,
    filled_slots: dict,
    missing_slots: List[str],
) -> str:
    return f"""
You are a Sri Lankan restaurant phone-call assistant speaking to a caller.

STATE: State 2 — Intent Discovery

Caller said:
\"\"\"{user_utterance}\"\"\"

Observed details explicitly stated by the caller:
{json.dumps(filled_slots, ensure_ascii=False)}

Still unknown details:
{json.dumps(missing_slots, ensure_ascii=False)}

Speech style:
Use natural spoken Sinhala typical of everyday Sri Lankan restaurant phone calls.
Keep the tone polite, respectful, customer-friendly, and conversational.
Prefer polite natural wording when appropriate.
Prefer Sinhala sentence structure and use English words only when they are commonly used in local speech (order, pickup, delivery).
Avoid translated English phrasing, robotic wording, or harsh language.

Rules:
- Do NOT mention intent labels like "{scenario["intent"]}".
- Base the reply on the caller utterance first.
- Use only details actually supported by the utterance.
- First respond naturally to the caller, then ask the best 1–3 short clarifying questions.
- Avoid repeating the caller's exact words.

Output format (MANDATORY):
<think>likely request; stated details; best next questions</think>
Then the final agent response text only.
""".strip()


def prompt_agent_response_state3(
    state_name: str,
    scenario: dict,
    user_utterance: str,
    filled_slots: dict,
    missing_slots: List[str],
) -> str:
    return f"""
You are a Sri Lankan restaurant phone-call assistant speaking to a caller.

STATE: {state_name}

Caller said:
\"\"\"{user_utterance}\"\"\"

Known details from the caller:
{json.dumps(filled_slots, ensure_ascii=False)}

Missing details needed to continue:
{json.dumps(missing_slots, ensure_ascii=False)}

Speech style:
Use natural spoken Sinhala typical of everyday Sri Lankan restaurant phone calls.
Keep the tone polite, respectful, customer-friendly, and conversational.
Prefer polite natural wording when appropriate.
Prefer Sinhala sentence structure and use English words only when they are commonly used in local speech (order, pickup, delivery).
Avoid translated English phrasing, robotic wording, or harsh language.
Keep the response clear, warm, and professional while still sounding natural.

Rules:
- Do NOT mention intent labels like "{scenario["intent"]}".
- Do NOT invent facts not stated by the caller.
- Use the known details above as grounded context.
- Respond naturally first, then ask 1–3 short questions for the most important missing details if needed.
- Avoid repeating the caller’s words exactly.
- If nothing important is missing, give a helpful final response.

Output format (MANDATORY):
<think>caller goal; confirmed details; missing details to ask next</think>
Then the final agent response text only.
""".strip()


# ----------------------------
# Validation helpers
# ----------------------------
def extracted_matches_sampled(
    sampled_filled: Dict[str, str],
    extracted_filled: Dict[str, str],
) -> bool:
    """
    Simple validation: every extracted slot should be in sampled_filled.
    We do not require exact string match for every slot because the generator
    may phrase some values differently, but we reject unknown extracted slots.
    """
    for key in extracted_filled.keys():
        if key not in sampled_filled:
            return False
    return True


# ----------------------------
# Row builders
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
    }

    if not validate_scenario(scenario):
        return None

    sig = scenario_signature(scenario)
    if sig in used_sigs:
        return None
    used_sigs.add(sig)

    user_utt = llm_text(
        prompt_user_utterance_state2("State 2: Intent Discovery", scenario)
    )

    slots_json = llm_text(prompt_extract_slots(intent, user_utt))
    parsed = safe_json_loads(slots_json)

    if parsed and isinstance(parsed.get("filled_slots"), dict) and isinstance(parsed.get("missing_slots"), list):
        filled_slots = parsed["filled_slots"]
        missing_slots = parsed["missing_slots"]
    else:
        filled_slots = {}
        missing_slots = SLOT_SCHEMA.get(intent, [])

    agent_out = llm_text(
        prompt_agent_response_state2(
            scenario,
            user_utt,
            filled_slots,
            missing_slots,
        )
    )

    instruction = "You are a Breezi Sinhala Call Agent. Identify the caller’s request and ask 1–3 clarifying questions."
    context_memory = "Call answered and greeted. Line clear. Start intent discovery."

    return {
        "instruction": instruction,
        "input": {
            "current_state": "State 2: Intent Discovery",
            "intent": intent,
            "filled_slots": filled_slots,
            "missing_slots": missing_slots,
            "user_utterance": user_utt,
            "context_memory": context_memory,
        },
        "output": agent_out,
    }


def build_state3_row(row_index: int, used_sigs: set) -> Optional[dict]:
    intent = random.choice(INTENTS)
    visible_slots, missing_slots = pick_visible_missing(intent)
    sampled_filled_slots = sample_slot_values(intent, visible_slots)

    scenario = {
        "intent": intent,
        "caller_type": random.choice(CALLER_TYPES),
        "context": random.choice(CONTEXTS),
        "style": random.choice(STYLES),
        "variation": random.choice(VARIATIONS),
        "state": "State 3: Slot Filling",
        "visible_slots": visible_slots,
        "missing_slots": missing_slots,
    }

    if not validate_scenario(scenario):
        return None

    sig = scenario_signature(scenario)
    if sig in used_sigs:
        return None
    used_sigs.add(sig)

    user_utt = llm_text(
        prompt_user_utterance_state3(
            "State 3: Slot Filling",
            scenario,
            sampled_filled_slots,
            missing_slots,
        )
    )

    slots_json = llm_text(prompt_extract_slots(intent, user_utt))
    parsed = safe_json_loads(slots_json)

    if parsed and isinstance(parsed.get("filled_slots"), dict):
        extracted_filled = parsed["filled_slots"]
    else:
        extracted_filled = {}

    filled_slots = sampled_filled_slots

    if parsed and not extracted_matches_sampled(sampled_filled_slots, extracted_filled):
        return None

    agent_out = llm_text(
        prompt_agent_response_state3(
            "State 3: Slot Filling",
            scenario,
            user_utt,
            filled_slots,
            missing_slots,
        )
    )

    instruction = "You are a Breezi Sinhala Call Agent. Ask targeted questions to fill missing details."
    context_memory = (
        f"Restaurant call. Caller type: {scenario['caller_type']}. "
        f"Context: {scenario['context']}. Style: {scenario['style']}."
    )

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
        "output": agent_out,
    }


# ----------------------------
# Main: generate N rows and save JSONL
# ----------------------------
def generate_jsonl(path: str, total_rows: int = 20, state2_ratio: float = 0.5):
    """
    state2_ratio=0.5 means ~50% State 2 rows, ~50% State 3 rows.
    """
    used_sigs = set()
    rows_written = 0
    attempts = 0
    max_attempts = total_rows * 20

    with open(path, "w", encoding="utf-8") as f:
        while rows_written < total_rows and attempts < max_attempts:
            attempts += 1
            do_state2 = random.random() < state2_ratio

            row = (
                build_state2_row(rows_written + 1, used_sigs)
                if do_state2
                else build_state3_row(rows_written + 1, used_sigs)
            )

            if row is None:
                continue

            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            rows_written += 1

    print(f"Wrote {rows_written} rows to {path}")
    if rows_written < total_rows:
        print(f"Stopped early after {attempts} attempts.")


if __name__ == "__main__":
    generate_jsonl("restaurant_test_21.jsonl", total_rows=20, state2_ratio=0.5)