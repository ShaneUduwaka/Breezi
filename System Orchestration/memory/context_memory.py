from typing import Dict, Any, List


class ContextMemory:
    """In-memory storage for conversational context (states/turns).

    Each session is identified by a `session_id`.  We maintain two data
    structures in memory:
      * session_states: dict storing the latest state for each session.
      * session_turns: dict storing list of turn records for each session.

    The turn list is trimmed to `max_turns` (default 100) so old history is dropped.
    """

    def __init__(self, max_turns: int = 100):
        """Initialize in-memory context storage.
        
        Args:
            max_turns: Maximum number of turns to keep per session (default 100)
        """
        self.max_turns = max_turns
        self.session_states = {}  # {session_id: state_dict}
        self.session_turns = {}   # {session_id: [turn_dict, ...]}

    def save(self, session_id: str, state: Dict[str, Any]) -> None:
        """Save the most recent intent state for the session."""
        self.session_states[session_id] = state

    def load(self, session_id: str) -> Dict[str, Any]:
        """Retrieve the saved state for the given session (or empty dict)."""
        return self.session_states.get(session_id, {})

    def append_turn(self, session_id: str, turn: Dict[str, Any]) -> None:
        """Append a turn record (user input + agent output + metadata)."""
        if session_id not in self.session_turns:
            self.session_turns[session_id] = []
        
        self.session_turns[session_id].append(turn)
        
        # Keep list trimmed to max_turns
        if len(self.session_turns[session_id]) > self.max_turns:
            self.session_turns[session_id] = self.session_turns[session_id][-self.max_turns:]

    def get_turns(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieve all turns for a session."""
        return self.session_turns.get(session_id, [])

    def clear(self, session_id: str) -> None:
        """Remove all stored data for a session."""
        self.session_states.pop(session_id, None)
        self.session_turns.pop(session_id, None)
