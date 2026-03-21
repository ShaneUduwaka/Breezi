import os

# Path to the data file where contacts will be stored
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CONTACTS_FILE_PATH = os.path.join(DATA_DIR, "contacts.json")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
