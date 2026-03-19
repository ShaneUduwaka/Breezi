class DialogOrchestrator:
    def __init__(self, registry, llm):
        self.registry = registry
        self.llm = llm
        self.current_language = "english"

    def process(self, state, language="english"):
        """Process state with language support (english or sinhala_mixed)"""
        self.current_language = language
        use_sinhala = language != "english"

        if not state.intent:
            response = "I didn't understand what you want. Could you please rephrase?"
            if use_sinhala:
                from utils.sinhala_utils import format_sinhala_response
                response = format_sinhala_response(response)
            return response

        intent_def = self.registry.get_intent(state.intent)

        if not intent_def:
            response = "Sorry, I cannot handle that request."
            if use_sinhala:
                from utils.sinhala_utils import format_sinhala_response
                response = format_sinhala_response(response)
            return response

        missing = state.missing_slots()

        if missing:
            return self._handle_missing_slots(state, missing, use_sinhala)

        return self._handle_complete(state, use_sinhala)

    def _handle_missing_slots(self, state, missing, use_sinhala):
        """Handle missing slots with language support"""
        if self.llm:
            prompt = self._build_llm_prompt(state, missing)
            response = self.llm.generate(prompt)
            if use_sinhala:
                from utils.sinhala_utils import format_sinhala_response
                response = format_sinhala_response(response)
            return response

        response = state.get_next_prompt() or "Please provide the required information."+str(missing)
        if use_sinhala:
            from utils.sinhala_utils import format_sinhala_response
            response = format_sinhala_response(response)
        return response

    def _build_llm_prompt(self, state, missing):
        return {
            "intent": state.intent,
            "slots": state.slots,
            "missing": missing,
            "message": "Please ask the user for missing information."
        }

    def _handle_complete(self, state, use_sinhala):
        """Execute handler with language support"""
        handler = self.registry.get_handler(state.intent)

        if not handler:
            return "Request completed."

        try:
            return handler(state, use_sinhala=use_sinhala)
        except TypeError:
            return handler(state)

