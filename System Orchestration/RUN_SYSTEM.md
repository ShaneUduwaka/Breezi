# How to Run the Breezi System

---

## 🚀 OPTION 1: Run Full Demo (Start Here - Easiest)

### Single Command:

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
python main.py
```

### What It Does:

Runs a complete 4-turn conversation demo showing:

- ✅ System boots up
- ✅ Configuration loads from JSON
- ✅ Full conversation flow
- ✅ Intent recognition
- ✅ Slot filling
- ✅ Multilingual responses (English + Sinhala)

### Example Output:

```
================================================================================
🚀 BREEZI AI CALL AGENT - TEMPLATE-BASED MODE
================================================================================

📋 Loading test scenarios from configuration...
⚙️ Initializing all system components...

Turn 1:
User: "I want to order a pizza"
Bot: "I need some information: order_type, quantity_per_item. Could you..."

Turn 2:
User: "delivery"
Bot: "I need some information: delivery_address, quantity_per_item..."

Turn 3:
User: "2 pizzas"
Bot: "I need some information: delivery_address. Could you provide..."

Turn 4:
User: "123 Main Street"
Bot: "✓ ඉල්ලුම ආරම්භ කරන ලදි! ඔබ අවශ්‍ය කරන්නේ: ['pizza']..." (Response in Sinhala)

✅ DEMO COMPLETE - All components working!
```

**Duration:** ~30 seconds  
**When to use:** To quickly verify the entire system is working

---

## 🌐 OPTION 2: Run API Server (Interactive Web Testing)

### Step 1: Start the Server

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
uvicorn api:app --reload
```

### Expected Output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
[16:35:45] INFO     Application startup complete
```

### Step 2: Open a NEW PowerShell Terminal (keep server running!)

### Step 3: Test the API

#### A. Health Check

```powershell
curl http://localhost:8000/health
```

Expected Response:

```json
{ "status": "healthy" }
```

#### B. Get Configuration

```powershell
curl http://localhost:8000/config
```

Expected Response:

```json
{
  "business_name": "Breezi Fast Food",
  "type": "restaurant",
  "intents": 16,
  "menu_categories": ["burgers", "buckets", "sides"]
}
```

#### C. Send a Chat Message

```powershell
curl -X POST http://localhost:8000/message `
  -H "Content-Type: application/json" `
  -d '{
    "text": "I want to order pizza",
    "session_id": "user123",
    "language": "en"
  }'
```

Expected Response:

```json
{
  "response": "I need some information: order_type, quantity_per_item. Could you provide these details?",
  "intent": "start_order",
  "session_id": "user123",
  "language": "en"
}
```

#### D. Change Language (Sinhala)

```powershell
curl -X POST http://localhost:8000/message `
  -H "Content-Type: application/json" `
  -d '{
    "text": "පිසាවට ඕනෑයි",
    "session_id": "user123",
    "language": "si"
  }'
```

### Step 4: Stop the Server

Press `Ctrl+C` in the terminal running the server.

**Duration:** Runs indefinitely until you stop it (Ctrl+C)  
**When to use:** To interactively test the API, build a frontend, or integrate with other systems

---

## 🧪 OPTION 3: Run Validation Tests

### Quick Health Check (All Tests)

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
python VALIDATION_TEST.py
```

### Expected Output:

```
[TEST 1] JSON Configuration Loading - ✅ PASSED
[TEST 2] System Initialization - ✅ PASSED
[TEST 3] NLU Text Processing - ✅ PASSED
[TEST 4] Conversation Flow - ✅ PASSED
[TEST 5] Using Template Business Data - ✅ PASSED
[TEST 6] API Endpoints - ✅ PASSED
[TEST 7] Multilingual Support - ✅ PASSED

OVERALL STATUS: ✅ FULLY FUNCTIONAL & PRODUCTION READY
```

**Duration:** ~30 seconds  
**When to use:** To verify all components are working before deployment

---

## 📊 Comparison

| Option         | Command                     | Time       | Use Case                          |
| -------------- | --------------------------- | ---------- | --------------------------------- |
| **Demo**       | `python main.py`            | 30 sec     | Quick system verification         |
| **API Server** | `uvicorn api:app --reload`  | Indefinite | Interactive testing, integrations |
| **Tests**      | `python VALIDATION_TEST.py` | 30 sec     | Component health check            |

---

## ⚠️ Troubleshooting

### Error: "No such file or directory"

**Problem:** You're not in the correct folder  
**Solution:**

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
pwd  # Verify you're in the right place
```

### Error: "python: command not found"

**Problem:** Python not in PATH  
**Solution:** Use full path:

```powershell
&"C:/Program Files/Python313/python.exe" main.py
```

### Error: "Port 8000 already in use" (when running API server)

**Problem:** Another process is using port 8000  
**Solution:** Use a different port:

```powershell
uvicorn api:app --reload --port 8001
```

Then test on `http://localhost:8001`

### Error: "ModuleNotFoundError"

**Problem:** Dependencies not installed  
**Solution:** Install them:

```powershell
&"C:/Program Files/Python313/python.exe" -m pip install fastapi uvicorn redis httpx
```

---

## ✨ What's Happening When You Run It?

### During `python main.py`:

1. **Loads configuration** from `Business input/intent.JSON`
2. **Initializes 14 components** (NLU, Dialog, Handlers, etc.)
3. **Loads test scenarios** from `Business input/testdata.JSON`
4. **Runs a simulated conversation** with 4 turns
5. **Demonstrates multilingual support** (English + Sinhala)
6. **Shows response generation** based on intents and slots
7. **Completes successfully** ✅

### During `uvicorn api:app`:

1. **Starts FastAPI server** on port 8000
2. **Loads configuration** from `Business input/intent.JSON`
3. **Initializes 14 components**
4. **Open endpoints:**
   - `GET /health` - Check if system is running
   - `GET /config` - Get business configuration
   - `POST /message` - Send a message and get response
   - `WebSocket /ws` - Real-time communication (if implemented)
5. **Stays running** until you press Ctrl+C

---

## 🎯 Recommended Flow

### First Time?

1. Start with `python main.py` to see the system work
2. Then try `python VALIDATION_TEST.py` to verify all components
3. Finally run `uvicorn api:app --reload` and test endpoints with curl

### Want to Test Interactively?

1. Start the API server: `uvicorn api:app --reload`
2. Send different messages to `http://localhost:8000/message`
3. Try different languages (en, si)
4. Try different intents (order, menu, delivery, etc.)

### Want to Build a Frontend?

1. API server is already running and ready
2. Send POST requests to `http://localhost:8000/message`
3. Build UI around the response

---

## 📝 Next Steps

**Choose one:**

- ✅ Run the demo: `python main.py`
- ✅ Start the API: `uvicorn api:app --reload`
- ✅ Run tests: `python VALIDATION_TEST.py`

All are ready to go! Pick one and let's see it work! 🚀
