# Breezi Contacts API Backend

This is the FastAPI backend that handles the Contact Us form submissions from the Breezi website.

## Requirements

- Python 3.8+
- Node.js (for the frontend)

## Installation

1. Navigate to this directory in your terminal:
   ```bash
   cd "c:\Users\MN\OneDrive\Documents\Breezi\MarketingWebsite\backend"
   ```

2. (Optional but recommended) Create and activate a virtual environment.

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Backend

Start the development server:

```bash
uvicorn main:app --reload
```

The server will start on `http://localhost:8000`. 
- The API endpoint is available at `POST http://localhost:8000/api/contact/`.
- You can view the interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Data Storage

Submitted contacts are stored in JSON format at `data/contacts.json`. This file is created automatically when the first submission is received.
