from dialog.intent_state import IntentState


class ConversationManager:

    def __init__(self, registry, orchestrator, nlu):
        self.registry = registry
        self.orchestrator = orchestrator
        self.nlu = nlu

        self.state = None

    def handle_message(self, text):

        nlu_result = self.nlu.parse(text)

        if self.state is None or nlu_result.intent != self.state.intent:

            intent_def = self.registry.get_intent(nlu_result.intent)

            if not intent_def:
                return "Sorry, I don't understand."

            self.state = IntentState(nlu_result.intent, intent_def)

        for slot, value in nlu_result.entities.items():
            self.state.update_slot(slot, value)

        return self.orchestrator.process(self.state)