from typing import Any, Optional


class RagStore:
    """In-memory key/value store for retrieval-augmented data.

    This is intentionally minimal: you can `put` any JSON-serializable value and
    later `get` it by key.  Handlers can use it to look up menu text, documents,
    or other blobs without reloading the business JSON file.
    """

    def __init__(self):
        """Initialize in-memory key/value store."""
        self.store = {}  # {key: value}

    def put(self, key: str, value: Any) -> None:
        """Store a value under `key`.  Overwrites existing data."""
        self.store[key] = value

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a previously-stored value (or ``None`` if missing)."""
        return self.store.get(key, None)

    def delete(self, key: str) -> None:
        """Remove a key from the store."""
        self.store.pop(key, None)
