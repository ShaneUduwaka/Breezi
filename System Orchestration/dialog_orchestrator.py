class DialogOrchestrator:
    def __init__(self, registry, llm, handlers):
        """
        registry: intent definitions (your JSON)
        llm: LLM service for prompting (optional but recommended)
        handlers: mapping of handler names -> functions
        """
        self.registry = registry
        self.llm = llm
        self.handlers = handlers

    def process(self, state):
        """
        Main dialog decision function.

        state: IntentState instance
        returns response message
        """

        # 1) If no intent -> cannot process (ask intent or error)
        if not state.intent:
            return "I didn’t understand what you want. Could you please rephrase?"

        # 2) Get intent definition
        definition = self.registry.get(state.intent)
        if not definition:
            return "Sorry, I cannot handle that request."

        # 3) Check missing required slots
        missing = state.missing_slots()

        if missing:
            # Slots are missing -> ask user (LLM or direct prompt)
            return self._handle_missing_slots(state, definition, missing)

        # 4) All slots filled -> call handler
        return self._handle_complete(state, definition)

    def _handle_missing_slots(self, state, definition, missing):
        # Option A: use LLM to generate question
        if self.llm:
            prompt = self._build_llm_prompt(state, definition, missing)
            return self.llm.generate(prompt)

        # Option B: fallback to first missing slot prompt
        slot_name = missing[0]
        slot_def = definition["slots"][slot_name]
        return slot_def.get("prompt") or "Please provide the required information."
