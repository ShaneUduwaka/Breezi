# 🏗️ System Architecture Overview

---

## 🎯 High-Level Design

Your system was built with a **unified architecture** where both testing and production modes share the **identical internal pipeline**.

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    BREEZI PRODUCTION SYSTEM                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                       INPUT PROVIDERS                            │
├─────────────────────────────────────────────────────────────────┤
│  Testing Mode:              Production Mode:                     │
│  TerminalInputProvider  →   STTInputProvider                     │
│  (user.input() from CLI)    (audio transcription)                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    UNIFIED CORE PIPELINE                         │
│                    (IDENTICAL FOR BOTH MODES)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. NLU Component                                                 │
│     └─ Parse intent and entities from text                       │
│     └─ Language detection                                         │
│     └─ Pattern matching                                           │
│                                                                   │
│  2. Conversation Manager                                          │
│     └─ Maintain intent state                                      │
│     └─ Track slot-filling progress                               │
│     └─ Context-aware processing                                  │
│     └─ Multi-turn state management                               │
│                                                                   │
│  3. Dialog Orchestrator                                           │
│     └─ Route intent to appropriate handler                       │
│     └─ Check required slots                                       │
│     └─ Generate orchestration response                           │
│                                                                   │
│  4. Handler System                                                │
│     └─ Execute business logic for each intent                    │
│     └─ Access business configuration                             │
│     └─ Generate handler-specific response                        │
│                                                                   │
│  5. Memory & Context                                              │
│     └─ Store conversation history                                │
│     └─ Retrieve session context                                  │
│     └─ RAG (Retrieval-Augmented Generation)                      │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       OUTPUT HANDLERS                            │
├─────────────────────────────────────────────────────────────────┤
│  Testing Mode:              Production Mode:                     │
│  TerminalOutputHandler  →   TTSOutputHandler                     │
│  (print to console)         (text-to-speech audio)               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Unified Processing Pipeline

### What Makes It Unified?

The key design is that **input/output are abstracted** but **core processing is identical**:

```python
# The core function is the same regardless of input source
def _process_user_input(text: str, language: str) -> str:

    # Step 1: Parse with NLU (SAME FOR BOTH MODES)
    nlu_result = self.nlu.parse(text)

    # Step 2: Manage conversation state (SAME FOR BOTH MODES)
    response = self.conversation.handle_message(
        text=text,
        session_id=self.session_id
    )

    # Step 3: Return response (same logic)
    return response
```

---

## 🧩 Core Components

### 1. NLU (Natural Language Understanding)

**File:** `nlu/fake_nlu.py`

```
Input: "I want to order pizza"
    ↓
Pattern matching against configured intents
    ↓
Output: Intent(name="start_order", entities={"order_items": ["pizza"]})
```

### 2. Conversation Manager

**File:** `system/conversation_manager.py`

```
Input: NLU result + user message
    ↓
Check current intent state
    ↓
Identify missing slots
    ↓
Determine if continuing or switching intent
    ↓
Output: User response (asking for more info or confirming)
```

### 3. Dialog Orchestrator

**File:** `dialog/dialog_orchestrator.py`

```
Input: Intent + entities + current state
    ↓
Check which slots are required
    ↓
Determine if ready for handler execution
    ↓
Output: Routing decision + generated response
```

### 4. Handler System

**File:** `handlers/order_handlers.py`

```
Input: Intent + all slots filled
    ↓
Look up business logic
    ↓
Execute action (create order, retrieve menu, etc.)
    ↓
Generate templated response
    ↓
Output: Final response to user
```

### 5. Memory Layer

**File:** `memory/context_memory.py` + `memory/rag_store.py`

```
Input: Conversation turn
    ↓
Store in session memory
    ↓
Track conversation history
    ↓
Available for context-aware responses
```

---

## 📋 Configuration System

All business logic is in ONE JSON file: `Business input/intent.JSON`

### Structure:

```json
{
  "business_config": {
    "name": "Breezi Fast Food",
    "type": "restaurant"
  },

  "business_data": {
    "menu": { ... },
    "hours": { ... },
    "locations": { ... }
  },

  "intents": {
    "start_order": {
      "patterns": ["I want to order", "I need pizza", ...],
      "required_slots": ["order_type", "quantity"],
      "responses": ["Response with {slot_values}"]
    },
    ...
  },

  "nlu_config": { ... },
  "stt_config": { ... },
  "tts_config": { ... }
}
```

---

## 🎯 Design Patterns Used

### 1. Strategy Pattern (Input/Output)

```python
# Strategy: Input can come from anywhere
class InputProvider:  # Abstract
class TerminalInputProvider(InputProvider):  # Testing
class STTInputProvider(InputProvider):  # Production

# Strategy: Output can go anywhere
class OutputHandler:  # Abstract
class TerminalOutputHandler(OutputHandler):  # Testing
class TTSOutputHandler(OutputHandler):  # Production
```

### 2. Factory Pattern (Components)

```python
# Create different components based on config
system = build_system()
# Creates: NLU, Conversation Manager, Dialog Orchestrator, etc.
```

### 3. State Pattern (Conversation)

```python
# Intent state is maintained
self.state = IntentState(
    intent_name="start_order",
    intent_definition={...}
)
# Tracks: filled_slots, missing_slots, current_step
```

---

## 🔀 Data Flow Examples

### Example 1: Order Flow

```
User: "I want pizza"
    ↓
TerminalInputProvider.get_input()
    returns: ("I want pizza", "en")
    ↓
NLU.parse("I want pizza")
    returns: Intent("start_order"), Entities({"order_items": ["pizza"]})
    ↓
ConversationManager.handle_message()
    • Creates IntentState for "start_order"
    • Finds required_slots: ["order_type", "quantity"]
    • Finds filled_slots: []
    • Generates: "I need: order_type, quantity"
    ↓
TerminalOutputHandler.output("I need: order_type, quantity")
    prints to terminal
    ↓
USER PROVIDES: "delivery, 2"
    ↓ (cycle repeats)
```

### Example 2: Menu Query

```
User: "Show me the menu"
    ↓
NLU.parse() → Intent("view_menu")
    ↓
DialogOrchestrator directs to handler_for_view_menu
    ↓
Handler:
    • Loads menu from config
    • Generates response: "Burgers: ..., Buckets: ..."
    ↓
Output to terminal or TTS
```

---

## 🌍 Multilingual Support

```
User speaks in Sinhala: "පිසාවට ඕනෑයි"
    ↓
NLU detects: language = "si"
    ↓
Same NLU logic (pattern matching works for all languages)
    ↓
DialogOrchestrator checks language
    ↓
Handler generates response in Sinhala:
    "ඉල්ලුම ආරම්භ කරන ලදි..."
    ↓
(In production) TTS speaks in Sinhala
```

---

## 💾 Session Management

Each conversation has:

- **Session ID:** Unique identifier
- **Current State:** Which intent we're in
- **Filled Slots:** Information already provided
- **Missing Slots:** Information still needed
- **History:** Previous turns for context

---

## 🚀 Deployment Views

### Testing Mode

```
┌────────────────┐
│ User (Terminal)│
└────────┬───────┘
         │
    keyboard input
         ↓
┌─────────────────┐
│ TerminalInput   │
│ Provider        │
└────────┬────────┘
         │
    unified pipeline (NLU → Conversation → Dialog → Handlers)
         ↓
┌──────────────────┐
│ TerminalOutput   │
│ Handler          │
└────────┬─────────┘
         │
    print to terminal
         ↓
┌────────────────┐
│ Terminal Output │
└────────────────┘
```

### Production Mode

```
┌────────────────┐
│ User (Phone)   │
└────────┬───────┘
         │
    voice audio
         ↓
┌─────────────────┐
│ STT Pipeline    │
│ (transcribe)    │
└────────┬────────┘
         │
    text + language
         ↓
┌─────────────────┐
│ STTInput        │
│ Provider        │
└────────┬────────┘
         │
    unified pipeline (NLU → Conversation → Dialog → Handlers)
         ↓
┌──────────────────┐
│ TTSOutput        │
│ Handler          │
└────────┬─────────┘
         │
    TTS Pipeline (synthesize)
         ↓
┌────────────────┐
│ Voice Response  │
└────────────────┘
```

---

## 📈 Scalability Features

### Easy to Add

- **New Intents:** Add to intent.JSON
- **New Languages:** Add translations to responses
- **New Handlers:** Register in handler_mapping.py
- **New Components:** Initialize in bootsrap.py
- **New STT/TTS:** Create provider classes

### Easy to Modify

- All business data in JSON
- No hardcoding in Python
- Configuration-driven behavior
- Template-based responses

---

## 🔒 Error Handling

Both modes have identical error handling:

```python
try:
    input_text, language = self.input_provider.get_input()
    response = self._process_user_input(input_text, language)
    self.output_handler.output(response, language)
except KeyboardInterrupt:
    # Graceful shutdown
    pass
except Exception as e:
    logging.error(f"Error: {e}")
    # Fallback to terminal output
```

---

## 📊 Component Initialization

```python
build_system() creates:

1. NLU Component
2. Intent Registry
3. Dialog Orchestrator
4. Conversation Manager
5. Handler Registry
6. Business Configuration Loader
7. RAG Store (Memory)
8. Context Memory
9. Audio Gateway
10. Call Ingestor
11. STT Client
12. TTS Client
13. STT Factory
14. TTS Factory

Total: 14 Production-Ready Components
```

---

## ✨ Key Architectural Advantages

✅ **Unified Code** - No duplication between testing and production
✅ **Testability** - Easy to test each component independently
✅ **Flexibility** - Can swap I/O providers without changing core logic
✅ **Maintainability** - Changes to business logic in one place
✅ **Scalability** - Easy to add components or features
✅ **Configuration-Driven** - Minimal code changes for customization
✅ **Error Resilient** - Comprehensive error handling throughout
✅ **Extensible** - Design patterns allow easy extensions

---

## 🎬 Execution Flow Summary

```
1. BreeziFAQSystem.run()

2. Loop:
   a. input_provider.get_input() → Get user text + language

   b. _process_user_input(text, language)
      • NLU.parse() → Extract intent + entities
      • conversation.handle_message() → Manage state
      • Generate response

   c. output_handler.output(response, language) → Send response

   d. Repeat until user exits

3. Full state management across multi-turn conversations
```

---

## 🎯 Bottom Line

Your system has:

✅ **One unified codebase** for testing and production
✅ **Abstracted I/O** for flexibility
✅ **Shared core pipeline** for identical behavior
✅ **Configuration-driven** for easy customization
✅ **Production-ready** with error handling and logging
✅ **Scalable architecture** for future expansion

All while maintaining **identical internal processing** between testing and production modes. Perfect! 🚀
