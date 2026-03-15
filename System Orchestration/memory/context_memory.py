import json
import time
from typing import Dict, Any, List

# optionally import redis
try:
    import redis
except ImportError:
    redis = None


class ContextMemory:
    """Persist conversational context (states/turns) in Redis.

    Each session is identified by a `session_id`.  We maintain two data
    structures:
      * a hash under key ``session_id`` containing the latest serialized state.
      * a list ``{session_id}:turns`` holding recent turn records.

    The list is trimmed to `max_turns` (default 100) so old history is dropped.
    """

    def __init__(self, redis_url: str, max_turns: int = 100):
        if redis is None:
            print("⚠️ ContextMemory: redis library not installed, operating in-memory only")
            self._r = None
            self.max_turns = max_turns
            return
        try:
            self._r = redis.from_url(redis_url)
            self._r.ping()
        except Exception as e:
            print(f"⚠️ ContextMemory: unable to connect to Redis ({e}), operating in-memory only")
            self._r = None
        self.max_turns = max_turns

    def save(self, session_id: str, state: Dict[str, Any]) -> None:
        """Persist the most recent intent state for the session."""
        if not self._r:
            return
        try:
            self._r.hset(session_id, mapping={"state": json.dumps(state)})
        except Exception:
            pass

    def load(self, session_id: str) -> Dict[str, Any]:
        """Retrieve the saved state for the given session (or empty dict)."""
        if not self._r:
            return {}
        try:
            data = self._r.hget(session_id, "state")
        except Exception:
            return {}
        if not data:
            return {}
        return json.loads(data)

    def append_turn(self, session_id: str, turn: Dict[str, Any]) -> None:
        """Append a turn record (user input + agent output + metadata)."""
        if not self._r:
            return
        key = f"{session_id}:turns"
        try:
            self._r.rpush(key, json.dumps(turn))
            # keep list trimmed to max_turns
            self._r.ltrim(key, -self.max_turns, -1)
        except Exception:
            pass

    def get_turns(self, session_id: str) -> List[Dict[str, Any]]:
        if not self._r:
            return []
        try:
            raw = self._r.lrange(f"{session_id}:turns", 0, -1)
        except Exception:
            return []
        return [json.loads(r) for r in raw]

    def clear(self, session_id: str) -> None:
        """Remove all stored data for a session."""
        if not self._r:
            return
        try:
            self._r.delete(session_id)
            self._r.delete(f"{session_id}:turns")
        except Exception:
            pass
