import json

class IntentRegistry:
    def __init__(self, path, handler_mapping=None):
        self.handler_mapping = handler_mapping or {}
        self.intents = self.load_schema(path)

    def load_schema(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        registry = {}
        for intent_id, intent_data in data["intents"].items():
            handler_name = intent_data.get("handler")
            intent_data["_handler_func"] = self.handler_mapping.get(handler_name)
            registry[intent_id] = intent_data

        return registry

    def get_intent(self, intent_id):
        return self.intents.get(intent_id)

    def get_slots(self, intent_id):
        intent = self.get_intent(intent_id)
        return intent.get("slots", {}) if intent else {}

    def get_handler(self, intent_id):
        intent = self.get_intent(intent_id)
        return intent.get("_handler_func") if intent else None