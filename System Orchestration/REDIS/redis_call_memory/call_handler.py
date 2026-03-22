from config import RECENT_MESSAGE_COUNT
from memory_store import (
    add_message,
    get_recent_messages,
    get_all_messages,
    add_summary,
    get_summary,
    set_metadata,
    get_metadata,
    update_metadata,
)


def start_call(call_id: str, phone_number: str = None, caller_name: str = None) -> None:
    """
    Start a new call with optional metadata.
    """
    add_message(call_id, "system", "Call started")

    metadata = {
        "call_id": call_id,
        "start_time": __import__("time").time(),
        "status": "active",
    }
    if phone_number:
        metadata["phone_number"] = phone_number
    if caller_name:
        metadata["caller_name"] = caller_name

    set_metadata(call_id, metadata)


def end_call(call_id: str) -> None:
    """
    Mark call as ended and save final status.
    """
    add_message(call_id, "system", "Call ended")
    update_metadata(call_id, {"status": "ended"})


def save_user_message(call_id: str, text: str) -> None:
    add_message(call_id, "user", text)


def save_agent_message(call_id: str, text: str) -> None:
    add_message(call_id, "agent", text)


def get_recent_context_text(call_id: str, limit: int = RECENT_MESSAGE_COUNT) -> str:
    """
    Turn the latest messages into plain text.
    Good for passing into an LLM later.
    """
    messages = get_recent_messages(call_id, limit=limit)

    lines = []
    for msg in messages:
        speaker = msg["speaker"].capitalize()
        text = msg["text"]
        lines.append(f"{speaker}: {text}")

    return "\n".join(lines)


def get_full_transcript_text(call_id: str) -> str:
    """
    Turn the entire stored call into plain text.
    """
    messages = get_all_messages(call_id)

    lines = []
    for msg in messages:
        speaker = msg["speaker"].capitalize()
        text = msg["text"]
        lines.append(f"{speaker}: {text}")

    return "\n".join(lines)


def build_prompt_for_ai(
    call_id: str,
    latest_user_input: str,
    use_summary: bool = True,
    limit: int = RECENT_MESSAGE_COUNT
) -> str:
    """
    Build a prompt string using recent call memory and optional summary.
    For long calls, combining summary + recent messages is better than
    dumping everything to the LLM.
    """
    context_parts = []

    # Add summary if available and requested
    if use_summary:
        summary = get_summary(call_id)
        if summary:
            context_parts.append(f"[Older conversation summary]\n{summary}\n")

    # Add recent messages
    recent = get_recent_context_text(call_id, limit=limit)
    if recent:
        context_parts.append(f"[Recent messages]\n{recent}")

    context = "\n".join(context_parts) if context_parts else "[No previous context]"

    prompt = f"""You are a helpful phone call assistant.

Call context:
{context}

Latest user message:
User: {latest_user_input}

Reply naturally, using the call context when helpful.
"""
    return prompt


def get_call_info(call_id: str) -> dict:
    """
    Get metadata and message count for a call.
    """
    metadata = get_metadata(call_id) or {}
    all_messages = get_all_messages(call_id)

    return {
        **metadata,
        "message_count": len(all_messages),
    }
