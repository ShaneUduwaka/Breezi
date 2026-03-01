class IntentState:
    def __init__(self, intent_name, intent_definition):
        self.intent = intent_name
        self.definition = intent_definition

        # slot storage
        self.slots = {}
        self.slot_status = {}  # filled / missing

        # initialize slot status
        for slot_name in intent_definition.get("slots", {}):
            self.slots[slot_name] = None
            self.slot_status[slot_name] = "missing"

        self.completed = False
        self.substate = "INIT"  # optional dialog substate

    def update_slot(self, slot_name, value):
        if slot_name in self.slots:
            self.slots[slot_name] = value
            self.slot_status[slot_name] = "filled"

    def is_complete(self):
        # all required slots filled?
        for name, meta in self.definition.get("slots", {}).items():
            if meta.get("required") and self.slots.get(name) is None:
                return False
        return True

    def missing_slots(self):
        return [
            name for name, meta in self.definition.get("slots", {}).items()
            if meta.get("required") and self.slots.get(name) is None
        ]

    def get_next_prompt(self):
        # return prompt for first missing slot
        for name in self.missing_slots():
            return self.definition["slots"][name].get("prompt")
        return None

    def to_dict(self):
        return {
            "intent": self.intent,
            "slots": self.slots,
            "slot_status": self.slot_status,
            "completed": self.completed,
            "substate": self.substate
        }