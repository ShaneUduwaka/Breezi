from dialog.intent_state import IntentState
import time


class ConversationManager:

    def __init__(self, registry, orchestrator, nlu, memory=None):
        self.registry = registry
        self.orchestrator = orchestrator
        self.nlu = nlu
        # optional ContextMemory instance
        self.memory = memory
        # last-used session id
        self.session_id = None

        self.state = None

    def handle_message(self, text, session_id: str = None):
        """Process a user utterance.

        ``session_id`` is used to save and load context if a ContextMemory is
        configured.  The method will update the ongoing intent state and then
        invoke the dialog orchestrator.  After the handler response is
        generated the turn is appended to memory along with serialized state.
        """

        # maintain session identifier for subsequent calls
        if session_id:
            self.session_id = session_id

        nlu_result = self.nlu.parse(text)

        if self.state is None or nlu_result.intent != self.state.intent:

            intent_def = self.registry.get_intent(nlu_result.intent)

            if not intent_def:
                response = "Sorry, I don't understand."
                self._maybe_append_turn(text, nlu_result, response)
                return response

            self.state = IntentState(nlu_result.intent, intent_def)

        for slot, value in nlu_result.entities.items():
            self.state.update_slot(slot, value)

        response = self.orchestrator.process(self.state)

        # save conversation state and turn
        self._maybe_append_turn(text, nlu_result, response)

        return response

    def _maybe_append_turn(self, text, nlu_result, response):
        if not self.memory or not self.session_id:
            return

        turn = {
            "input": text,
            "intent": nlu_result.intent,
            "slots": self.state.slots if self.state else {},
            "output": response,
            "timestamp": time.time(),
        }
        try:
            self.memory.append_turn(self.session_id, turn)
            # also persist latest state
            if self.state:
                self.memory.save(self.session_id, self.state.to_dict())
        except Exception:
            # swallow memory errors so conversation continues even if Redis fails
            pass