# main.py
import os
from IntentRegistry import IntentRegistry  # your class

# 1. Get the directory of this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Build path to the JSON
json_path = os.path.join(current_dir, "..", "Business input", "intent.JSON")

# 3. Normalize to absolute path
json_path = os.path.abspath(json_path)

print("Loading JSON from:", json_path)

# 4. Create handler mapping
def start_order(context):
    print("Placing order:", context)


handlers = {"handle_start_order": start_order}

# 5. Create registry
registry = IntentRegistry(json_path, handler_mapping=handlers)

# Test it
print(registry.get_intent("start_order"))

print (registry.get_handler("start_order"))

handler=registry.get_handler("start_order")

handler({"item": "pizza", "quantity": 2})

