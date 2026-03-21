import json
import time
import redis

from config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    CALL_MEMORY_TTL_SECONDS,
)

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
)


def _call_key(call_id: str, suffix: str = "messages") -> str:
    """
    Build a Redis key for a call with given suffix.
    Examples: call:A123:messages, call:A123:summary, call:A123:meta
    """
    return f"call:{call_id}:{suffix}"


def add_message(call_id: str, speaker: str, text: str) -> None:
    """
    Save one message from the call into Redis.
    """
    key = _call_key(call_id, "messages")

    message = {
        "speaker": speaker,
        "text": text,
        "timestamp": int(time.time())
    }

    redis_client.rpush(key, json.dumps(message))
    redis_client.expire(key, CALL_MEMORY_TTL_SECONDS)


def get_recent_messages(call_id: str, limit: int = 10) -> list[dict]:
    """
    Get the latest N messages from the call.
    """
    key = _call_key(call_id, "messages")

    items = redis_client.lrange(key, -limit, -1)

    messages = []
    for item in items:
        messages.append(json.loads(item))

    return messages


def get_all_messages(call_id: str) -> list[dict]:
    """
    Get the full stored conversation for one call.
    """
    key = _call_key(call_id, "messages")

    items = redis_client.lrange(key, 0, -1)

    messages = []
    for item in items:
        messages.append(json.loads(item))

    return messages


def add_summary(call_id: str, summary_text: str) -> None:
    """
    Save a summary of older call parts (for long calls).
    """
    key = _call_key(call_id, "summary")
    redis_client.set(key, summary_text)
    redis_client.expire(key, CALL_MEMORY_TTL_SECONDS)


def get_summary(call_id: str) -> str | None:
    """
    Get the stored summary for a call (or None if not set).
    """
    key = _call_key(call_id, "summary")
    return redis_client.get(key)


def set_metadata(call_id: str, metadata: dict) -> None:
    """
    Save metadata for a call (phone number, start time, status, etc).
    """
    key = _call_key(call_id, "meta")
    redis_client.set(key, json.dumps(metadata))
    redis_client.expire(key, CALL_MEMORY_TTL_SECONDS)


def get_metadata(call_id: str) -> dict | None:
    """
    Get the metadata for a call (or None if not set).
    """
    key = _call_key(call_id, "meta")
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None


def update_metadata(call_id: str, updates: dict) -> None:
    """
    Update specific metadata fields without overwriting others.
    """
    key = _call_key(call_id, "meta")
    existing = get_metadata(call_id) or {}
    existing.update(updates)
    redis_client.set(key, json.dumps(existing))
    redis_client.expire(key, CALL_MEMORY_TTL_SECONDS)


def clear_call(call_id: str) -> None:
    """
    Delete all stored data for a call (messages, summary, metadata).
    """
    for suffix in ["messages", "summary", "meta"]:
        key = _call_key(call_id, suffix)
        redis_client.delete(key)


def call_exists(call_id: str) -> bool:
    """
    Check whether this call already has memory in Redis.
    """
    key = _call_key(call_id, "messages")
    return redis_client.exists(key) == 1
