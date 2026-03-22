# 🎬 Run The System NOW - Step by Step

---

## ⚡ The Fastest Way to Get Started

### 1. Open PowerShell

Open a new PowerShell terminal

### 2. Navigate to the System

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
```

### 3. Run the System in Testing Mode

```powershell
python system.py --mode testing
```

### 4. You Should See

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
```

### 5. Type Your First Command

```
👤 You: I want to order a pizza
```

### 6. You'll Get a Response

```
 [System Processing...]
  Intent: start_order
  Entities: {'order_items': ['pizza']}

🤖 Bot: I need some information: order_type, quantity_per_item.
        Could you provide these details?
```

### 7. Continue the Conversation

```
👤 You: delivery, 2
🤖 Bot: I need some information: delivery_address.
        Could you provide this?

👤 You: 123 Main Street
🤖 Bot: ✓ Order confirmed! You ordered: pizza

👤 You: exit
👋 Goodbye!
```

---

## 🎯 What to Try

After starting the system, try these inputs:

### Order Something

```
I want to order a pizza
I'd like a burger
Can I get 2 buckets?
```

### Browse Menu

```
Show me the menu
What burgers do you have?
Tell me about sides
```

### Ask Questions

```
What are your hours?
Where are you located?
Do you deliver?
```

### View Options

```
menu
(Shows this list of available commands)
```

### Exit

```
exit
quit
q
```

---

## 🔄 Understanding What's Happening

When you type something, here's what happens internally:

```
You type: "I want to order pizza"
    ↓
System receives input
    ↓
NLU parses: Intent=start_order, Items=pizza
    ↓
Conversation Manager: "This is a start_order. Need slots: order_type, quantity"
    ↓
Dialog Orchestrator: Routes to order_handlers
    ↓
Handler executes logic, generates response
    ↓
Bot responds: "I need: order_type, quantity_per_item..."
    ↓
You continue conversation...
```

**Important:** Testing and Production modes use the **EXACT SAME** internal pipeline!

---

## 📊 Expected Behavior

### Multi-Turn Conversation

The system tracks what you're doing:

- **Turn 1:** You start an order
- **Turn 2:** System asks for missing info
- **Turn 3:** You provide more info
- **Turn 4:** System confirms and finalizes

### Language Detection

System automatically detects:

- English: Default
- Sinhala: When you type Sinhala characters

### State Management

System remembers:

- What you've said before
- What information you provided
- What's still needed
- Your language preference

---

## 🎨 Your Screen Layout

When running, you'll see:

```
====== Startup Banner ======
Shows: Mode, Business, Intents, Menu Categories

====== Turn 1 ======
You: (type here)
Bot: (responds here)

====== Turn 2 ======
You: (type here)
Bot: (responds here)

... (repeats for each turn)
```

---

## 🚀 When You're Done Testing

### Option 1: Test Something Else

```powershell
# System is still running, just type something else
You: Show me the menu
```

### Option 2: Start Over

```powershell
You: exit
(then run again)
python system.py --mode testing
```

### Option 3: Try Another Mode

```powershell
You: exit
(then run production mode)
python system.py --mode production
```

---

## ⚙️ Troubleshooting

### Issue: Nothing happens when I type

**Solution:** Press Enter to submit your input

### Issue: Command not found

**Solution:** Make sure you're in the right directory:

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
pwd  # Check you're there
```

### Issue: Python not found

**Solution:** Try with full path:

```powershell
&"C:/Program Files/Python313/python.exe" system.py --mode testing
```

### Issue: "ModuleNotFoundError"

**Solution:** Install dependencies:

```powershell
&"C:/Program Files/Python313/python.exe" -m pip install fastapi uvicorn redis httpx
```

---

## 📋 What You Can Do

✅ **Test intent recognition** - Try various phrases  
✅ **Test multi-turn** - Have a full conversation  
✅ **Test slot filling** - Provide information step by step  
✅ **Test multilingual** - Try Sinhala text  
✅ **Test state management** - Verify system remembers context  
✅ **Test error handling** - Try weird inputs  
✅ **Test response generation** - See different responses

---

## 📈 Testing Checklist

After a few interactions, check:

- [ ] System accepted my input
- [ ] Intent was recognized correctly
- [ ] Bot asked for missing information
- [ ] When I provided info, bot acknowledged it
- [ ] Bot maintained context across turns
- [ ] Responses made sense
- [ ] System didn't crash or error

---

## 🎓 Learning More

After trying the system:

1. **Read QUICK_START.md** - Overview of capabilities
2. **Read PRODUCTION_DEPLOYMENT_GUIDE.md** - Detailed operations
3. **Check DELIVERY_SUMMARY.md** - What was built and why
4. **Look at system.py** - See how it's implemented (380 lines, well-commented)

---

## 🎬 Action Items

### Right Now (Next 2 minutes)

1. Open PowerShell
2. Navigate to System Orchestration folder
3. Run `python system.py --mode testing`
4. Type `I want to order a pizza`
5. Continue the conversation

### That's It!

The system is production-ready and working. You're just testing it to verify.

---

## ✨ Key Things to Remember

1. **Same Internal Logic** - Testing and production modes use identical pipeline
2. **Configuration-Driven** - All data comes from `Business input/intent.JSON`
3. **Multi-Turn Support** - System tracks state across messages
4. **Multilingual** - Auto-detects language
5. **Production Ready** - Has error handling, logging, session management

---

## 🎯 Next Steps After Testing

1. **Test thoroughly** - Try various scenarios
2. **Verify behavior** - Make sure it works as expected
3. **Consider production** - When ready, run `--mode production`
4. **Deploy** - Point it to real STT/TTS services

---

## 🚀 GO!

```powershell
cd "c:\Users\harry\OneDrive\Documents\GitHub\Breezi new\Breezi\System Orchestration"
python system.py --mode testing
```

**Start now!** 🎬
