class IntentState:
    def __init__(self, intent_name, intent_definition):
        self.intent = intent_name
        self.definition = intent_definition

        slots = intent_definition.get("slots", {})

        self.slots = {name: None for name in slots}
        self.slot_status = {name: "missing" for name in slots}

        self.completed = False
        self.substate = "INIT"

    def update_slot(self, slot_name, value):
        if slot_name in self.slots:
            self.slots[slot_name] = value
            self.slot_status[slot_name] = "filled"

    def is_complete(self):
        for name, meta in self.definition.get("slots", {}).items():
            if meta.get("required") and self.slots.get(name) is None:
                return False
        return True

    def missing_slots(self):
        missing = []
        for name, meta in self.definition.get("slots", {}).items():
            # Check if slot is required
            is_required = meta.get("required", False)
            
            # Check conditional requirements based on dependencies
            if meta.get("dependencies"):
                # If this slot has dependencies, it's required only if dependencies are met
                dependencies = meta.get("dependencies", [])
                # For delivery_address: required only if order_type="delivery"
                if name == "delivery_address" and "order_type" in dependencies:
                    is_required = self.slots.get("order_type") == "delivery"
            
            # Add to missing if required and not filled
            if is_required and self.slots.get(name) is None:
                missing.append(name)
        
        return missing

    def get_next_prompt(self):
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