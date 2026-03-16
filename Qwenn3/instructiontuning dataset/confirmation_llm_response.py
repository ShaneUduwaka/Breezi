import os
import json
import time
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai

# ----------------------------
# Gemini client
# ----------------------------
load_dotenv(dotenv_path=".env")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-1.5-flash"

model = genai.GenerativeModel(MODEL)

def llm_text(prompt: str, *, max_retries: int = 3) -> str:
    last_err = None

    for attempt in range(max_retries):
        try:
            resp = model.generate_content(prompt)

            text = resp.text.strip()

            if not text:
                raise RuntimeError("Empty response")

            return text

        except Exception as e:
            last_err = e
            time.sleep(0.8 * (attempt + 1))

    raise RuntimeError(f"LLM call failed after retries: {last_err}")


def prompt_agent_response_state4(intent: str, user_utterance: str, filled_slots: dict, missing_slots: List[str]) -> str:
    return f"""
You are a Sri Lankan restaurant staff member speaking to a caller on the phone.

STATE: State 4 — Confirmation & Audit

Caller said:
\"\"\"{user_utterance}\"\"\"

Known details:
{json.dumps(filled_slots, ensure_ascii=False)}

Missing details:
{json.dumps(missing_slots, ensure_ascii=False)}

Speech style:
Use natural spoken Sinhala used in real Sri Lankan restaurant phone calls.
Keep the tone polite, brief, and conversational.
Prefer spoken Sinhala sentence structure.
Use English words only when commonly used in local speech, such as order, pickup, delivery, number, time.
Avoid translated English phrasing.
Avoid formal written Sinhala.
Avoid robotic or chatbot-like wording.
Do not use numbered lists.
Do not over-explain.

Response rules:
- Do NOT mention intent labels like "{intent}".
- Do NOT invent facts not stated by the caller.
- First respond briefly to the caller’s confirmation, concern, or final change.
- Then ask only about the exact missing details if needed.
- If nothing is missing, give one short helpful final response.
- Keep the whole response short and practical.

Output format (MANDATORY):
<think>SHORT PLAN (<=20 words). Checklist only. No step-by-step reasoning.</think>
Then the final agent response text (no extra tags).
""".strip()


def generate_state4_responses(input_path: str, output_path: str):

    rows = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))

    completed_rows = []

    for row in rows:

        intent = row["input"]["intent"]
        filled_slots = row["input"]["filled_slots"]
        missing_slots = row["input"]["missing_slots"]
        user_utterance = row["input"]["user_utterance"]

        agent_out = llm_text(
            prompt_agent_response_state4(
                intent=intent,
                user_utterance=user_utterance,
                filled_slots=filled_slots,
                missing_slots=missing_slots
            )
        )

        row["output"] = agent_out
        completed_rows.append(row)

    with open(output_path, "w", encoding="utf-8") as f:
        for row in completed_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Wrote {len(completed_rows)} rows to {output_path}")


if __name__ == "__main__":
    generate_state4_responses(
        input_path="state4_user_rows.jsonl",
        output_path="state4_completed_rows.jsonl"
    )