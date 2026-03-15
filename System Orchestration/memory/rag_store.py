import json
from typing import Any, Optional

# redis may not be available in certain environments (demo/test).
try:
    import redis
except ImportError:
    redis = None


class RagStore:
    """Simple Redis-backed key/value store for retrieval-augmented data.

    This is intentionally minimal: you can `put` any JSON-serializable value and
    later `get` it by key.  Handlers can use it to look up menu text, documents,
    or other blobs without reloading the business JSON file.
    """

    def __init__(self, redis_url: str):
        if redis is None:
            print("⚠️ RagStore: redis library not installed, operating in-memory only")
            self._r = None
            return
        try:
            self._r = redis.from_url(redis_url)
            # probe connection
            self._r.ping()
        except Exception as e:
            # Redis not available; degrade silently to in-memory
            print(f"⚠️ RagStore: unable to connect to Redis ({e}), operating in-memory only")
            self._r = None

    def put(self, key: str, value: Any) -> None:
        """Store a value under `key`.  Overwrites existing data."""
        if not self._r:
            return
        try:
            self._r.set(key, json.dumps(value))
        except Exception:
            pass

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a previously-stored value (or ``None`` if missing)."""
        if not self._r:
            return None
        try:
            data = self._r.get(key)
        except Exception:
            return None
        if data is None:
            return None
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            # store may contain plain strings
            return data.decode("utf-8")

    def delete(self, key: str) -> None:
        """Remove a key from the store."""
        if not self._r:
            return
        try:
            self._r.delete(key)
        except Exception:
            pass
