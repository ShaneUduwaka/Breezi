# Breezi Production System - Deployment Guide

---

## 🚀 What's New

✅ **Unified Architecture**: Same internal processing for testing and production  
✅ **Two Modes**: Testing (terminal) and Production (STT)  
✅ **Production Ready**: Full system with error handling and logging  
✅ **Easy Switching**: One command to switch between modes

---

## 🧪 TESTING MODE (Interactive Testing)

### Run the System in Testing Mode

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
python system.py --mode testing
```

### What You Get

- ✅ Terminal input (type your questions)
- ✅ Same internal NLU, dialog, handler pipeline as production
- ✅ Real-time state management
- ✅ Multi-turn conversations
- ✅ Multilingual support (English + Sinhala)
- ✅ Full logging and debugging

### Example Session

```
======================================================================
🚀 BREEZI SYSTEM - PRODUCTION READY
======================================================================
Mode: 🧪 TESTING
Business: Breezi Fast Food
Type: restaurant
Intents: 16
Menu Categories: 3
======================================================================

📝 Interactive Testing Mode
   • Type natural language questions
   • Type 'exit' or 'quit' to end session
   • Type 'menu' to see available options
   • All processing uses production pipeline

⏳ System ready. Processing inputs...

======================================================================
📥 TURN 1
======================================================================
👤 You: I want to order a pizza

🤖 Bot: I need some information: order_type, quantity_per_item. Could you provide these details?

======================================================================
📥 TURN 2
======================================================================
👤 You: delivery, 2 pizzas

🤖 Bot: I need some information: delivery_address. Could you provide this?

======================================================================
📥 TURN 3
======================================================================
👤 You: 123 Main Street

🤖 Bot: ✓ Order confirmed! You ordered: pizza

👋 Goodbye!
```

### Available Commands

| Command              | Action                  |
| -------------------- | ----------------------- |
| `menu`               | Show available commands |
| `exit` or `quit`     | Exit the system         |
| Any natural language | Process as user input   |

---

## 📞 PRODUCTION MODE (STT Pipeline)

### Run the System in Production Mode

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
python system.py --mode production
```

### What It Does

- ✅ Listens to audio input (STT)
- ✅ Processes through **identical** pipeline as testing
- ✅ Responds via TTS (text-to-speech)
- ✅ Real-time conversation
- ✅ Automatic language detection
- ✅ Full production logging

### Production Flow

```
User speaks
    ↓
STT Pipeline (transcribe audio)
    ↓
NLU (parse intent + entities)
    ↓
Conversation Manager (maintain state)
    ↓
Dialog Orchestrator (route to handler)
    ↓
Handler (execute business logic)
    ↓
TTS Pipeline (synthesize response)
    ↓
Response played to user
```

---

## 🏗️ System Architecture

### Unified Core Pipeline

Both testing and production modes use the **identical internal processing**:

```python
# 1️⃣ INPUT
User Input → Terminal (testing) or STT (production)

# 2️⃣ PROCESSING (IDENTICAL FOR BOTH)
↓ NLU: Parse intent and entities
↓ Conversation Manager: Maintain state, slot-filling
↓ Dialog Orchestrator: Route to handler
↓ Handler: Execute business logic
↓ Response Generation

# 3️⃣ OUTPUT
Response → Terminal (testing) or TTS (production)
```

### Key Components

| Component                | Purpose                                     | Status              |
| ------------------------ | ------------------------------------------- | ------------------- |
| **NLU**                  | Intent recognition and entity extraction    | ✅ Production Ready |
| **Conversation Manager** | State management and multi-turn context     | ✅ Production Ready |
| **Dialog Orchestrator**  | Route intents to handlers                   | ✅ Production Ready |
| **Handlers**             | Execute business logic (orders, menu, etc.) | ✅ Production Ready |
| **Memory**               | Store context and conversation history      | ✅ Production Ready |
| **Configuration**        | All data from JSON (no hardcoding)          | ✅ Production Ready |

---

## 📊 Testing Workflow

### Scenario: Build and Test Before Production

```
1. Test with terminal input
   python system.py --mode testing

   ✅ Verify intents work
   ✅ Test conversation flow
   ✅ Check slot filling
   ✅ Validate responses

2. Once satisfied, deploy to production
   python system.py --mode production

   ✅ Real STT input
   ✅ Real TTS output
   ✅ Same internal logic
   ✅ Identical behavior
```

---

## 🎯 Key Features

### 1. Configuration-Driven

All business logic, intents, and menu items come from `Business input/intent.JSON`:

- No hardcoding in Python
- Change behavior by editing JSON
- Easy customization for different restaurants

### 2. Multi-Turn Conversations

System maintains state across turns:

- Tracks current intent
- Maps slots (order items, delivery address, etc.)
- Context-aware responses
- Handles incomplete inputs

### 3. Multilingual Support

Built-in support for multiple languages:

- English: Default
- Sinhala: Detected automatically
- Easy to add more languages

### 4. Production Ready

- ✅ Error handling and recovery
- ✅ Logging and monitoring
- ✅ Session management
- ✅ Timeout handling
- ✅ Graceful shutdown

---

## 📝 Usage Examples

### Test a Specific Scenario

```powershell
# Start testing mode
python system.py --mode testing

# Example conversation
You: Show me the menu
Bot: Menu categories available: [burgers, buckets, sides]

You: Tell me about burgers
Bot: Available burgers: Classic Burger ($5.99), Bacon Burger ($6.99)...

You: I want the bacon burger
Bot: Great! Bacon Burger added to order. Any other items?
```

### Test Order Flow

```powershell
python system.py --mode testing

You: I want to order
Bot: Welcome! What would you like to order?

You: pizza
Bot: I have pizza. Great choice! What size? And how many?

You: large, 2
Bot: Order confirmed: 2 Large Pizzas. Would you like delivery or pickup?

You: delivery
Bot: What's your delivery address?

You: 123 Main Street
Bot: ✅ Order placed! Estimated delivery: 30 minutes
```

---

## 🔧 Configuration & Customization

### Change Business Name

Edit `Business input/intent.JSON`:

```json
{
  "business_config": {
    "name": "Your Restaurant Name",
    "type": "restaurant"
  },
  ...
}
```

### Add New Intent

```json
{
  "intents": {
    "my_new_intent": {
      "patterns": ["trigger phrase 1", "trigger phrase 2"],
      "required_slots": ["slot1"],
      "responses": ["Response template with {slot1}"]
    }
  }
}
```

### Add Menu Items

```json
{
  "business_data": {
    "menu": {
      "categories": {
        "my_category": [
          { "name": "Item 1", "price": 9.99, "description": "..." },
          { "name": "Item 2", "price": 10.99, "description": "..." }
        ]
      }
    }
  }
}
```

---

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError"

```powershell
# Install dependencies
&"C:/Program Files/Python313/python.exe" -m pip install fastapi uvicorn redis httpx
```

### Issue: "FileNotFoundError: Business input/intent.JSON"

```powershell
# Ensure you're in correct directory
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
pwd  # Verify location
```

### Issue: STT not working (production mode)

Configure STT provider in `Business input/intent.JSON`:

```json
{
  "stt_config": {
    "provider": "google", // or "aws", "azure"
    "api_key": "your_key"
  }
}
```

### Issue: TTS not working (production mode)

Configure TTS provider in `Business input/intent.JSON`:

```json
{
  "tts_config": {
    "provider": "google", // or "aws", "azure"
    "api_key": "your_key"
  }
}
```

---

## 📊 System Status

| Component            | Testing Mode | Production Mode |
| -------------------- | ------------ | --------------- |
| NLU                  | ✅           | ✅              |
| Conversation Manager | ✅           | ✅              |
| Dialog Orchestrator  | ✅           | ✅              |
| Handlers             | ✅           | ✅              |
| Terminal I/O         | ✅           | ❌              |
| STT                  | ❌           | ✅              |
| TTS                  | ❌           | ✅              |
| Logging              | ✅ DEBUG     | ✅ INFO         |

---

## 🎯 Next Steps

1. **Test the System**

   ```powershell
   python system.py --mode testing
   ```

2. **Verify All Features**
   - Test different intents
   - Test multi-turn conversations
   - Test language detection

3. **Deploy to Production**

   ```powershell
   python system.py --mode production
   ```

4. **Monitor and Log**
   - Check logs for errors
   - Validate responses
   - Track conversation metrics

---

## 📞 Support

**Testing Questions?** Type `menu` in testing mode

**Need to add features?** Edit `Business input/intent.JSON`

**Issues?** Check logs: Look for error messages and refer to Troubleshooting section

---

## ✨ Summary

- ✅ **Production-ready unified system**
- ✅ **Testing mode with terminal input**
- ✅ **Production mode with STT/TTS**
- ✅ **Identical internal pipeline**
- ✅ **Configuration-driven (no hardcoding)**
- ✅ **Multi-turn conversations**
- ✅ **Multilingual support**
- ✅ **Full error handling**

**You're ready to run the system!** 🚀
