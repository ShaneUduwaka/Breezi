import json
import os

DATA_FILE = "data/subscribers.json"

def save_subscriber(email: str):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # Initialize file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    # Read current subscribers
    with open(DATA_FILE, "r") as f:
        subscribers = json.load(f)

    # Check for duplicates
    if email in subscribers:
        return {"status": "already_exists"}

    # Add new email and save
    subscribers.append(email)
    with open(DATA_FILE, "w") as f:
        json.dump(subscribers, f, indent=4)
    
    return {"status": "success"}