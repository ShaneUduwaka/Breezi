import os
import json
import random
import hashlib
import asyncio
import re
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv
from google import genai

# ============================================================
# Setup
# ============================================================
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-3.1-flash-lite-preview"
OUTPUT_FILE = "restaurant_intent_classification.jsonl"
TARGET_ROWS = 4000

# Speed controls
BATCH_SIZE = 20
CONCURRENCY = 8
MAX_RETRIES_PER_ROW = 3
RETRY_SLEEP_BASE = 0.12

# ============================================================
# Intents
# ============================================================
INTENTS = [
    "start_new_order", "add_item_to_order", "remove_item_from_order", "modify_item",
    "change_quantity", "view_current_cart", "clear_cart", "apply_coupon_promo",
    "ask_price_of_item", "ask_availability_of_item", "customize_item",
    "ask_for_recommendations", "confirm_order", "cancel_order_before_payment",
    "reorder_previous_order",

    "choose_payment_method", "ask_accepted_payment_types", "payment_failed",
    "confirm_payment", "refund_request", "split_payment", "ask_invoice_receipt",

    "choose_delivery", "choose_pickup", "change_delivery_address",
    "add_delivery_instructions", "ask_delivery_time_estimate", "track_order",
    "change_pickup_time", "report_delivery_issue", "report_missing_item",
    "late_delivery_complaint",

    "store_opening_hours", "store_location", "holiday_schedule",
    "parking_availability", "contact_details", "menu_inquiry",
    "nutritional_information", "allergen_information",

    "create_account", "login_help", "reset_password", "check_loyalty_points",
    "redeem_loyalty_points", "ask_membership_benefits", "update_profile_info",

    "file_complaint", "request_manager_callback", "report_bad_quality",
    "refund_complaint", "escalation_request", "feedback_submission",

    "ask_ongoing_offers", "ask_specific_promo",
    "subscribe_offers", "unsubscribe_marketing",

    "bulk_catering_order", "event_booking",
]

COMMON_INTENTS = [
    "start_new_order",
    "add_item_to_order",
    "choose_delivery",
    "choose_pickup",
    "menu_inquiry",
    "ask_price_of_item",
    "ask_availability_of_item",
    "customize_item",
    "change_quantity",
    "confirm_order",
    "track_order",
    "ask_delivery_time_estimate",
    "report_delivery_issue",
    "late_delivery_complaint",
    "store_opening_hours",
    "store_location",
    "ask_for_recommendations",
]

RARE_INTENTS = [i for i in INTENTS if i not in COMMON_INTENTS]

def sample_intent() -> str:
    if random.random() < 0.5:
        return random.choice(COMMON_INTENTS)
    return random.choice(RARE_INTENTS)

# ============================================================
# Scenario factors
# ============================================================
CALLER_PROFILES = [
    "student",
    "office worker",
    "nearby customer",
    "parent ordering for family",
    "regular customer",
    "first-time customer",
]

LIGHT_CONTEXTS = [
    "normal call",
    "quick call",
    "simple request",
    "calling casually",
    "calling after some thought",
    "short check before ordering",
]

TEMPOS = ["slow", "normal", "quick"]
TEMPO_WEIGHTS = [0.10, 0.72, 0.18]

DIRECTNESS = ["hinting", "indirect"]
DIRECTNESS_WEIGHTS = [0.75, 0.25]

MOODS = ["neutral", "pleasant"]
MOOD_WEIGHTS = [0.75, 0.25]

VERBOSITY = ["short"]
VERBOSITY_WEIGHTS = [1.0]

POLITENESS = ["medium", "high"]
POLITENESS_WEIGHTS = [0.60, 0.40]

# ============================================================
# Slot schema
# Used only as hint sources for this state
# ============================================================
SLOT_SCHEMA: Dict[str, List[str]] = {
    "start_new_order": ["food_item", "quantity", "order_type"],
    "add_item_to_order": ["order_id", "food_item", "quantity"],
    "remove_item_from_order": ["order_id", "food_item", "quantity"],
    "modify_item": ["order_id", "food_item", "modification_type"],
    "change_quantity": ["order_id", "food_item", "quantity"],
    "view_current_cart": ["order_id", "name", "phone_number"],
    "clear_cart": ["order_id", "name", "confirmation"],
    "apply_coupon_promo": ["order_id", "coupon_code", "promo_name"],
    "ask_price_of_item": ["food_item", "portion_size", "item_variant"],
    "ask_availability_of_item": ["food_item", "date", "item_variant"],
    "customize_item": ["food_item", "quantity", "special_request"],
    "ask_for_recommendations": ["food_preference", "price_range", "diet"],
    "confirm_order": ["order_id", "name", "status"],
    "cancel_order_before_payment": ["order_id", "reason", "urgency"],
    "reorder_previous_order": ["previous_order", "name", "phone_number"],

    "choose_payment_method": ["order_id", "payment_method", "amount"],
    "ask_accepted_payment_types": ["topic", "branch", "payment_method"],
    "payment_failed": ["order_id", "payment_method", "issue"],
    "confirm_payment": ["order_id", "payment_method", "amount"],
    "refund_request": ["order_id", "reason", "amount"],
    "split_payment": ["order_id", "split", "amount"],
    "ask_invoice_receipt": ["order_id", "type", "contact"],

    "choose_delivery": ["food_item", "quantity", "delivery_address"],
    "choose_pickup": ["food_item", "quantity", "pickup_time"],
    "change_delivery_address": ["order_id", "delivery_address", "landmark"],
    "add_delivery_instructions": ["order_id", "instructions", "landmark"],
    "ask_delivery_time_estimate": ["order_id", "delivery_address", "time"],
    "track_order": ["order_id", "phone_number", "name"],
    "change_pickup_time": ["order_id", "pickup_time", "name"],
    "report_delivery_issue": ["order_id", "issue", "resolution"],
    "report_missing_item": ["order_id", "food_item", "resolution"],
    "late_delivery_complaint": ["order_id", "issue", "delay"],

    "store_opening_hours": ["day", "time", "branch"],
    "store_location": ["branch", "area", "landmark"],
    "holiday_schedule": ["day", "holiday", "branch"],
    "parking_availability": ["branch", "time", "availability"],
    "contact_details": ["branch", "type", "time"],
    "menu_inquiry": ["category", "food_item", "price_range"],
    "nutritional_information": ["food_item", "portion", "nutrition"],
    "allergen_information": ["food_item", "allergen", "ingredient"],

    "create_account": ["name", "phone_number", "email"],
    "login_help": ["phone_number", "email", "issue"],
    "reset_password": ["phone_number", "email", "account"],
    "check_loyalty_points": ["phone_number", "name", "id"],
    "redeem_loyalty_points": ["id", "points", "order_id"],
    "ask_membership_benefits": ["type", "topic", "benefit"],
    "update_profile_info": ["account", "field", "value"],

    "file_complaint": ["order_id", "issue", "severity"],
    "request_manager_callback": ["name", "phone_number", "time"],
    "report_bad_quality": ["order_id", "food_item", "issue"],
    "refund_complaint": ["order_id", "issue", "amount"],
    "escalation_request": ["order_id", "issue", "previous"],
    "feedback_submission": ["order_id", "type", "message"],

    "ask_ongoing_offers": ["offer_type", "day", "category"],
    "ask_specific_promo": ["promo_name", "topic", "food_item"],
    "subscribe_offers": ["phone_number", "name", "contact"],
    "unsubscribe_marketing": ["phone_number", "email", "contact"],

    "bulk_catering_order": ["event_date", "headcount", "food_preference"],
    "event_booking": ["event_date", "event_time", "headcount"],
}

# ============================================================
# Helpers
# ============================================================
def normalize_text(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[“”\"'`´’]", "", text)
    return text.strip()

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def is_mostly_sinhala(text: str) -> bool:
    allowed = re.fullmatch(r"[A-Za-z\u0D80-\u0DFF0-9\s.,!?():\-/']+", text)
    if not allowed:
        return False
    sinhala_chars = len(re.findall(r"[\u0D80-\u0DFF]", text))
    english_chars = len(re.findall(r"[A-Za-z]", text))
    if sinhala_chars == 0:
        return False
    return english_chars <= sinhala_chars * 0.45 + 10

BAD_GENERIC_OPENERS = [
    "මට යමක් දැනගන්න තියෙනවා",
    "මට පොඩ්ඩක් දැනගන්න තියෙනවා",
    "පොඩ්ඩක් අහන්න තිබුණා",
    "යමක් අහන්න තිබුණා",
]

def has_bad_generic_opener(text: str) -> bool:
    t = normalize_text(text)
    return any(bad in t for bad in BAD_GENERIC_OPENERS)

def is_simple_user(text: str) -> bool:
    sentences = re.split(r"[.!?]+", text.strip())
    sentences = [s for s in sentences if s.strip()]
    if len(sentences) > 2:
        return False
    if len(text) > 90:
        return False
    return True

def scenario_signature(s: dict) -> str:
    small = {
        "intent": s["intent"],
        "hint_details": s["hint_details"],
        "caller_profile": s["caller_profile"],
        "light_context": s["light_context"],
        "tempo": s["tempo"],
        "directness": s["directness"],
        "mood": s["mood"],
        "verbosity": s["verbosity"],
        "politeness": s["politeness"],
    }
    return hash_text(json.dumps(small, sort_keys=True, ensure_ascii=False))

def pair_signature(user: str, assistant: str) -> str:
    return hash_text(normalize_text(user) + " || " + normalize_text(assistant))

def user_signature(user: str) -> str:
    return hash_text(normalize_text(user))

# ============================================================
# Hint selection
# Mostly 1 hint, sometimes 2
# ============================================================
def build_hints(intent: str) -> List[str]:
    slots = SLOT_SCHEMA[intent]
    if random.random() < 0.8:
        return [random.choice(slots)]
    return random.sample(slots, min(2, len(slots)))

# ============================================================
# Prompt
# ============================================================
def build_prompt(s: dict) -> str:
    return f"""
Create ONE realistic Sri Lankan restaurant phone-call training pair in spoken Sinhala for the state: Intent Classification.

=== LANGUAGE RULES ===
- Both user and assistant must be primarily in Sinhala.
- Use natural modern spoken Sinhala used in real Sri Lankan phone calls.
- A small amount of natural code-switching is okay when common in real speech.
- Do not overuse English.
- Do not use formal or textbook Sinhala.

=== USER (CALLER) REQUIREMENTS ===
- The caller should speak like a real person starting a phone call.
- The caller should hint the intent clearly but briefly.
- The caller should NOT explicitly state the intent label.
- The caller should NOT sound dramatic, mysterious, cinematic, or unrealistically vague.
- The caller should get to the actual purpose naturally and early.
- This state is NOT slot filling.
- Keep the user utterance lighter than a slot-filling example.
- Usually the caller should reveal only the main purpose and at most one supporting clue.
- Do NOT turn the utterance into a slot list.
- Do NOT give too much background, emotion, or explanation.
- Do NOT mention details outside the hint details below.
- Prefer ONE short sentence.
- Maximum TWO short sentences.

GOOD STYLE EXAMPLES:
- "චිකන් කොත්තුව තියෙනවද?"
- "මගේ order එක තාම ආවෙ නෑ"
- "හෙට රෑට open ද?"
- "මට pickup එකට දාගන්න පුළුවන්ද?"

=== ASSISTANT REQUIREMENTS ===
- The assistant must identify the likely caller intent from the utterance.
- The assistant should respond naturally first.
- Then ask the best next useful question or questions for that likely intent.
- The assistant should move the likely intent forward, not ask random generic questions.
- If the caller reports an issue, show understanding first, then ask the next relevant question.
- Keep the assistant natural, respectful, helpful, and brief.
- Do not sound robotic or scripted.

=== SHARED RULES ===
- The conversation must feel like a normal real restaurant phone call.
- The user should give LESS information than in slot filling.
- The assistant should do more of the work of identifying and narrowing the intent.
- Keep the exchange small, realistic, and useful.
- Avoid repetitive sentence patterns.

=== SCENARIO ===
Intent: {s["intent"]}
Hint details: {s["hint_details"]}
Caller profile: {s["caller_profile"]}
Light context: {s["light_context"]}
Tone: tempo={s["tempo"]}, directness={s["directness"]}, mood={s["mood"]}, verbosity={s["verbosity"]}
Assistant politeness: {s["politeness"]}

=== OUTPUT FORMAT (STRICT JSON) ===
{{
  "user": "...",
  "assistant": "..."
}}
""".strip()

# ============================================================
# Shared state for dedup
# ============================================================
seen_scenarios = set()
seen_users = set()
seen_pairs = set()
seen_lock = asyncio.Lock()

# ============================================================
# Scenario builder
# ============================================================
def make_scenario() -> dict:
    return {
        "intent": sample_intent(),
        "hint_details": [],
        "caller_profile": random.choice(CALLER_PROFILES),
        "light_context": random.choice(LIGHT_CONTEXTS),
        "tempo": random.choices(TEMPOS, TEMPO_WEIGHTS)[0],
        "directness": random.choices(DIRECTNESS, DIRECTNESS_WEIGHTS)[0],
        "mood": random.choices(MOODS, MOOD_WEIGHTS)[0],
        "verbosity": random.choices(VERBOSITY, VERBOSITY_WEIGHTS)[0],
        "politeness": random.choices(POLITENESS, POLITENESS_WEIGHTS)[0],
    }

# ============================================================
# Sync API call
# ============================================================
def _generate_sync(prompt: str) -> Optional[Tuple[str, str]]:
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "temperature": 0.95,
            "response_mime_type": "application/json",
        },
    )
    data = json.loads(response.text)
    return data["user"].strip(), data["assistant"].strip()

# ============================================================
# Async row generation
# ============================================================
async def generate_row_async(s: dict, sem: asyncio.Semaphore) -> Optional[dict]:
    scenario_sig = scenario_signature(s)

    async with seen_lock:
        if scenario_sig in seen_scenarios:
            return None
        seen_scenarios.add(scenario_sig)

    for attempt in range(MAX_RETRIES_PER_ROW):
        try:
            async with sem:
                user, assistant = await asyncio.to_thread(_generate_sync, build_prompt(s))

            if not user or not assistant:
                await asyncio.sleep(RETRY_SLEEP_BASE * (attempt + 1))
                continue

            if not is_mostly_sinhala(user) or not is_mostly_sinhala(assistant):
                await asyncio.sleep(RETRY_SLEEP_BASE * (attempt + 1))
                continue

            if has_bad_generic_opener(user):
                await asyncio.sleep(RETRY_SLEEP_BASE * (attempt + 1))
                continue

            if not is_simple_user(user):
                await asyncio.sleep(RETRY_SLEEP_BASE * (attempt + 1))
                continue

            u_sig = user_signature(user)
            p_sig = pair_signature(user, assistant)

            async with seen_lock:
                if u_sig in seen_users or p_sig in seen_pairs:
                    await asyncio.sleep(RETRY_SLEEP_BASE * (attempt + 1))
                    continue
                seen_users.add(u_sig)
                seen_pairs.add(p_sig)

            return {
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            f"You are a Breezi Sinhala Call Agent. "
                            f"State: intent_classification. "
                            f"Intent: {s['intent']}. "
                            f"Hint details: {s['hint_details']}. "
                            f"Caller type: {s['caller_profile']}. "
                            f"Context: {s['light_context']}. "
                            f"Identify the likely intent from the caller utterance and ask the next useful questions naturally."
                        ),
                    },
                    {"role": "user", "content": user},
                    {"role": "assistant", "content": assistant},
                ]
            }

        except Exception:
            await asyncio.sleep(RETRY_SLEEP_BASE * (attempt + 1))

    return None

# ============================================================
# Batch generation
# ============================================================
async def generate_batch(batch_size: int, sem: asyncio.Semaphore) -> List[dict]:
    scenarios = []
    for _ in range(batch_size):
        s = make_scenario()
        s["hint_details"] = build_hints(s["intent"])
        scenarios.append(s)

    tasks = [generate_row_async(s, sem) for s in scenarios]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]

# ============================================================
# Main
# ============================================================
async def run():
    written = 0
    sem = asyncio.Semaphore(CONCURRENCY)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        while written < TARGET_ROWS:
            need = min(BATCH_SIZE, TARGET_ROWS - written)
            rows = await generate_batch(need, sem)

            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
                written += 1

            if written > 0 and written % 100 == 0:
                print(f"{written} rows generated")

    print(f" DONE {written} rows")

if __name__ == "__main__":
    asyncio.run(run())