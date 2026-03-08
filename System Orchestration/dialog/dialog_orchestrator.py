class DialogOrchestrator:
    def __init__(self, registry, llm):
        self.registry = registry
        self.llm = llm

    def process(self, state):

        if not state.intent:
            return "I didn’t understand what you want. Could you please rephrase?"

        intent_def = self.registry.get_intent(state.intent)

        if not intent_def:
            return "Sorry, I cannot handle that request."

        missing = state.missing_slots()

        if missing:
            return self._handle_missing_slots(state, missing)

        return self._handle_complete(state)

    def _handle_missing_slots(self, state, missing):

        if self.llm:
            prompt = self._build_llm_prompt(state, missing)
            return self.llm.generate(prompt)

        return state.get_next_prompt() or "Please provide the required information."+str(missing)

    def _build_llm_prompt(self, state, missing):
        return {
            "intent": state.intent,
            "slots": state.slots,
            "missing": missing,
            "message": "Please ask the user for missing information."
        }

    def _handle_complete(self, state):

        handler = self.registry.get_handler(state.intent)

        if not handler:
            return "Request completed."

        return handler(state)

