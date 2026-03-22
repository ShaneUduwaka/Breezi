# Breezi System - Interactive Testing Guide

> **Run the system yourself and test all components interactively**

---

## 📋 Prerequisites

✅ Python 3.13+ installed  
✅ All dependencies installed (done)  
✅ Configuration files in place

---

## 🚀 OPTION 1: Run the Full Demo (Fastest - 1 minute)

### Step 1: Navigate to the System Orchestration folder

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
```

### Step 2: Run the interactive demo

```powershell
python main.py
```

### Expected Output:

```
================================================================================
🚀 BREEZI AI CALL AGENT - TEMPLATE-BASED MODE
================================================================================
Configuration: Loads ALL test data from testdata.JSON
No hardcoding in Python code - fully template-driven!

📋 Loading test scenarios from configuration...
[Demo running with 4-turn conversation]
Turn 1: User input → Bot responds
Turn 2: User input → Bot responds
Turn 3: User input → Bot responds
Turn 4: User input → Bot responds

✅ Success!
```

**What this tests:**

- ✅ JSON configuration loading
- ✅ System initialization (all 14 components)
- ✅ NLU (Natural Language Understanding)
- ✅ Multi-turn conversation flow
- ✅ Intent recognition
- ✅ Slot filling
- ✅ Response generation
- ✅ Multilingual support (English + Sinhala)

---

## 🌐 OPTION 2: Run the API Server (Interactive Testing - 2-3 minutes)

### Step 1: Start the FastAPI server

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Expected Output:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 2: Open a NEW PowerShell window and test endpoints

Keep the server running in Terminal 1, open Terminal 2:

#### Test 1: Health Check

```powershell
curl http://localhost:8000/health
```

**Expected Response:**

```json
{"status": "healthy", "components": [...]}
```

#### Test 2: Get Configuration

```powershell
curl http://localhost:8000/config
```

**Expected Response:**

```json
{
  "business_name": "Breezi Fast Food",
  "intents": 16,
  "menu_categories": ["burgers", "buckets", "sides"],
  ...
}
```

#### Test 3: Send a Message (Chat)

```powershell
curl -X POST http://localhost:8000/message `
  -H "Content-Type: application/json" `
  -d '{
    "text": "I want to order a pizza",
    "session_id": "test_123",
    "language": "en"
  }'
```

**Expected Response:**

```json
{
  "response": "I need some information: order_type, quantity_per_item. Could you provide...",
  "intent": "start_order",
  "session_id": "test_123",
  "language": "en"
}
```

### Step 4: Stop the server

Press `Ctrl+C` in Terminal 1 to stop the API server.

---

## 🧪 OPTION 3: Run Individual Component Tests

### Test the NLU (Intent Recognition)

```powershell
python -c "
from nlu.fake_nlu import NLU
from dialog.IntentRegistry import IntentRegistry
import json

# Load config
with open('Business input/intent.JSON', 'r') as f:
    config = json.load(f)

# Create NLU
nlu = NLU(config['nlu_config'])

# Test intent recognition
test_inputs = [
    'I want to order a pizza',
    'Show me the menu',
    'Tell me about burgers',
    'I want delivery'
]

print('\\n=== NLU TEST ===\\n')
for text in test_inputs:
    result = nlu.parse(text)
    print(f'Input: {text}')
    print(f'  Intent: {result[\"intent\"]}')
    print(f'  Entities: {result[\"entities\"]}')
    print()
"
```

**Expected Output:**

```
=== NLU TEST ===

Input: I want to order a pizza
  Intent: start_order
  Entities: {'order_items': ['pizza']}

Input: Show me the menu
  Intent: view_menu
  Entities: {}

Input: Tell me about burgers
  Intent: view_menu_item
  Entities: {'item_name': 'burger'}

Input: I want delivery
  Intent: global_browse
  Entities: {}
```

---

## 🔍 OPTION 4: Inspect the Configuration Files

### View the Business Configuration

```powershell
# View the full intent configuration
Get-Content "Business input/intent.JSON" | python -m json.tool | more

# View menu items
python -c "
import json
with open('Business input/intent.JSON') as f:
    config = json.load(f)
    print('\\n=== MENU STRUCTURE ===\\n')
    for category, items in config['business_data']['menu']['categories'].items():
        print(f'{category.upper()}:')
        for item in items:
            print(f'  - {item[\"name\"]}: \${item[\"price\"]}')
        print()
"
```

**Expected Output:**

```
=== MENU STRUCTURE ===

BURGERS:
  - Classic Burger: $5.99
  - Bacon Burger: $6.99
  - Deluxe Burger: $7.99

BUCKETS:
  - Small Bucket: $8.99
  - Medium Bucket: $12.99

SIDES:
  - Fries: $2.99
  - Coleslaw: $1.99
```

### View Intents

```powershell
python -c "
import json
with open('Business input/intent.JSON') as f:
    config = json.load(f)
    print('\\n=== INTENTS (Total: ' + str(len(config['intents'])) + ') ===\\n')
    for intent_name in list(config['intents'].keys())[:10]:
        print(f'- {intent_name}')
    print('  ... and more')
"
```

---

## ✅ Testing Checklist

After running the tests, verify these items:

### Configuration

- [ ] JSON file loads without errors
- [ ] Menu items display correctly (burgers, buckets, sides)
- [ ] Intents are recognized (16 total)
- [ ] Business name is "Breezi Fast Food"

### System Components

- [ ] Conversation manager initializes
- [ ] NLU processes text correctly
- [ ] Dialog orchestrator responds
- [ ] All 14 components boot without errors

### Functionality

- [ ] Intent recognition works (pizza → start_order)
- [ ] Multi-turn conversations maintain state
- [ ] Slots fill correctly (order_type, delivery_address, etc.)
- [ ] Responses generate based on intents

### Data Sources

- [ ] All menu data from JSON ✓
- [ ] All intents from JSON ✓
- [ ] All test data from JSON ✓
- [ ] NO hardcoded values ✓

### Languages

- [ ] English responses work ✓
- [ ] Sinhala responses work ✓
- [ ] Language auto-detection works ✓

### API (if testing Option 2)

- [ ] Health endpoint responds
- [ ] Config endpoint returns configuration
- [ ] Message endpoint processes text
- [ ] Session management works

---

## 🐛 Troubleshooting

### Issue: "Command not found: python"

**Solution:** Use full Python path:

```powershell
"C:/Program Files/Python313/python.exe" main.py
```

### Issue: "ModuleNotFoundError"

**Solution:** Reinstall dependencies:

```powershell
&"C:/Program Files/Python313/python.exe" -m pip install fastapi uvicorn redis httpx pytest responses
```

### Issue: "FileNotFoundError: Business input/intent.JSON"

**Solution:** Ensure you're in the correct directory:

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
pwd  # Verify current directory
```

### Issue: "Port 8000 already in use"

**Solution:** Use a different port:

```powershell
uvicorn api:app --reload --port 8001
```

---

## 📊 Summary

| Test              | Time    | Command                    | Tests                                |
| ----------------- | ------- | -------------------------- | ------------------------------------ |
| **Full Demo**     | 1 min   | `python main.py`           | Config, Init, NLU, Conv, Slots, Lang |
| **API Server**    | 2-3 min | `uvicorn api:app --reload` | Endpoints, Sessions, Config          |
| **Components**    | <1 min  | `python -c "..."`          | NLU only                             |
| **Configuration** | <1 min  | `Get-Content ...`          | Data structure, Intents, Menu        |

---

## ✨ You're All Set!

Choose any option above and run the tests yourself. All errors have been fixed and the system is ready to test.

**Start with Option 1** (Full Demo) for the quickest verification!
