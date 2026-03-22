import json
import os
import uuid
from datetime import datetime
from core.config import CONTACTS_FILE_PATH
from schemas.contact import ContactCreate

def _read_contacts() -> list:
    if not os.path.exists(CONTACTS_FILE_PATH):
        return []
    try:
        with open(CONTACTS_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def _write_contacts(contacts: list) -> None:
    with open(CONTACTS_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)

def save_contact_submission(contact: ContactCreate) -> dict:
    contacts = _read_contacts()
    
    # Create the new record with an ID and timestamp
    new_record = {
        "id": str(uuid.uuid4()),
        "name": contact.name,
        "email": contact.email,
        "company": contact.company,
        "message": contact.message,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # Append and save
    contacts.append(new_record)
    _write_contacts(contacts)
    
    return new_record
