# Breezi Real-Time Conversational AI - Complete Architecture Design

## 🎯 Overview

End-to-end architecture for real-time phone conversations with AI-powered order processing. Supports multiple call sources (Twilio, custom VoIP, etc.) with <200ms latency requirement.

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CALL INGESTION LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │   Twilio     │  │ Custom VoIP  │  │  WebRTC      │ (wrappers)   │
│  │  Webhook     │  │  (Asterisk)  │  │  Browser     │               │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘               │
│         │                 │                 │                       │
│         └─────────────────┼─────────────────┘                       │
└─────────────────────────────────────────────────────────────────────┘
                            │
                            ↓ (audio packets)
┌─────────────────────────────────────────────────────────────────────┐
│                  AUDIO STREAMING GATEWAY                            │
│  ├─ WebSocket Server (for real-time)                               │
│  ├─ Audio Buffer (jitter handling)                                 │
│  ├─ Codec handling (μ-law, opus, etc.)                             │
│  └─ Session routing                                                │
└─────────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ↓               ↓               ↓
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │     STT      │ │     SYSTEM   │ │     TTS      │
    │   Service    │ │ ORCHESTRATION│ │   Service    │
    │              │ │              │ │              │
    │ (Google/AWS/ │ │ ┌──────────┐ │ │ (Google/AWS/ │
    │  Azure/etc)  │ │ │NLU Engine│ │ │  Azure/etc)  │
    │              │ │ ├──────────┤ │ │              │
    └──────────────┘ │ │ Intent   │ │ └──────────────┘
                     │ │ Handlers │ │
                     │ ├──────────┤ │
                     │ │ State    │ │
                     │ │ Manager  │ │
                     │ └──────────┘ │
                     └──────────────┘
                            │
            ┌───────────────┼───────────────┐
            ↓               ↓               ↓
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │    Redis     │ │  Vector DB   │ │Client Data   │
    │   (sessions) │ │ (similarity) │ │   Base       │
    │              │ │              │ │  (wrapper)   │
    └──────────────┘ └──────────────┘ └──────────────┘
                            
                     ↓ (response audio)
┌─────────────────────────────────────────────────────────────────────┐
│                  AUDIO STREAMING GATEWAY                            │
│  Send audio frames back to caller                                   │
└─────────────────────────────────────────────────────────────────────┘
                            ↓
                      Back to Caller
```

---

## 🔄 Request-Response Flow (Real-Time)

```
Timeline: Each box = ~10-50ms

┌──────────────────────────────────────────────────────────────────┐
│ CALL FLOW WITH LATENCY BUDGET                                    │
├──────────────────────────────────────────────────────────────────┤

0ms   ┌─ Caller speaks "I want to order pizza"
      └─ Audio packets arrive (chunked) at Gateway

30ms  ┌─ STT starts processing audio chunks
      │  (buffering first 100ms of audio for better accuracy)
      └─ RTP/WebSocket streaming continues

150ms ┌─ STT completes: text = "I want to order pizza"
      │  (max STT latency: 100-150ms typical)
      └─ System Orchestration receives text

160ms ┌─ NLU processes: intent=start_order, entities={items:"pizza"}
      │  (processing: 10ms)
      └─ Handler triggered

170ms ┌─ Handler checks: do we need client DB?
      │  Option A: No DB lookup needed → continue
      │  Option B: Query client DB (optional, async)
      └─ Generate response: "Great! I'll start your pizza order"

180ms ┌─ TTS begins: convert response to audio
      │  (TTS latency: 50-100ms typical)
      └─ Parallel: More audio chunks arriving from caller

250ms ┌─ TTS completes: audio ready
      │  (total latency: 250ms - within budget!)
      └─ Audio Gateway sends frames back to caller

TOTAL: ~250ms end-to-end (acceptable for natural conversation)
```

---

## 🏗️ Component Details

### 1️⃣ CALL INGESTION LAYER (Wrapper Pattern)

**Purpose:** Abstract multiple call sources

```python
# adapters/call_ingestion/base.py
class CallIngestorBase:
    async def receive_audio_chunk(self) -> AudioChunk:
        """Receive audio frame from call source"""
        pass
    
    async def send_audio_chunk(self, audio: AudioChunk):
        """Send audio frame back to caller"""
        pass

# adapters/call_ingestion/twilio.py
class TwilioIngestor(CallIngestorBase):
    """Handle Twilio webhook audio"""
    pass

# adapters/call_ingestion/custom_voip.py
class CustomVoIPIngestor(CallIngestorBase):
    """Handle custom VoIP (Asterisk, FreeSWITCH)"""
    pass

# adapters/call_ingestion/webrtc.py
class WebRTCIngestor(CallIngestorBase):
    """Handle WebRTC browser audio"""
    pass
```

---

### 2️⃣ AUDIO STREAMING GATEWAY

**Purpose:** Real-time bidirectional audio handling

```python
# system/audio_gateway.py
class AudioStreamingGateway:
    """
    Manages real-time audio streaming with:
    - Low-latency buffering
    - Codec handling
    - Session routing
    """
    
    def __init__(self):
        self.active_sessions = {}  # session_id -> audio_buffer
        self.audio_buffer_size = 4000  # 250ms at 16kHz
    
    async def handle_incoming_audio(self, session_id, audio_chunk):
        """Process incoming audio"""
        # 1. Add to buffer
        # 2. Check if enough audio for STT
        # 3. Pass to STT when ready
        # 4. Route text to System Orchestration
        pass
    
    async def send_response_audio(self, session_id, audio_chunk):
        """Send response audio back"""
        # 1. Queue audio frames
        # 2. Send to caller via appropriate adapter
        pass
```

---

### 3️⃣ STT SERVICE (Speech-to-Text)

**Purpose:** Real-time speech recognition with streaming support

```python
# adapters/stt_client.py
class STTClient:
    """
    Multi-provider STT with streaming support
    Providers: Google Cloud Speech-to-Text, AWS Transcribe, Azure Speech
    """
    
    async def transcribe_stream(self, audio_stream, session_id):
        """
        Real-time streaming transcription
        Yields: TextResult(text, confidence, is_final)
        """
        pass

# Example usage
stt = STTClient(provider="google")
async for result in stt.transcribe_stream(audio_stream, session_id):
    if result.is_final:
        # Send to System Orchestration
        response = await orchestration.handle_message(
            result.text, 
            session_id=session_id
        )
```

---

### 4️⃣ SYSTEM ORCHESTRATION (Enhanced)

**Core flow with DB integration:**

```python
# system/conversation_manager.py (ENHANCED)
class ConversationManager:
    
    async def handle_message(self, text, session_id):
        # 1. NLU Processing
        nlu_result = self.nlu.parse(text)
        
        # 2. Intent Processing
        intent_handler = self.get_handler(nlu_result.intent)
        
        # 3. STATE MANAGEMENT
        state = self.state_manager.get_state(session_id)
        
        # 4. HANDLER EXECUTION (with optional DB lookup)
        response = await intent_handler.execute(
            nlu_result,
            state,
            client_db_accessor=self.client_db  # PASS DB ACCESSOR
        )
        
        # 5. Save state
        await self.state_manager.save_state(session_id, state)
        
        return response

# handlers/order_handlers.py (ENHANCED)
class StartOrderHandler:
    
    async def execute(self, nlu_result, state, client_db_accessor):
        # Check if we need to fetch menu from client DB
        if state.needs_menu_refresh():
            # Query client database for current menu/stock
            menu = await client_db_accessor.get_menu()
            stock = await client_db_accessor.get_stock()
            
            # Update internal state with fresh data
            state.update_menu(menu)
            state.update_stock(stock)
        
        # Continue with order processing
        # ...
        
        return response
```

---

### 5️⃣ TTS SERVICE (Text-to-Speech)

**Purpose:** Real-time speech synthesis with streaming

```python
# adapters/tts_client.py
class TTSClient:
    """
    Multi-provider TTS with streaming support
    Providers: Google Cloud Text-to-Speech, AWS Polly, Azure Speech
    """
    
    async def synthesize_stream(self, text, session_id, language="en"):
        """
        Real-time streaming synthesis
        Yields: AudioChunk(audio_bytes, duration)
        """
        pass

# Example usage
tts = TTSClient(provider="google")
async for audio_chunk in tts.synthesize_stream(response_text):
    await audio_gateway.send_response_audio(session_id, audio_chunk)
```

---

### 6️⃣ CLIENT DATABASE ABSTRACTION

**Purpose:** Wrapper pattern for different DB types

```python
# adapters/client_db/base.py
class ClientDatabaseBase:
    """Abstract base for client database access"""
    
    async def get_menu(self) -> Menu:
        """Get current menu items"""
        pass
    
    async def get_stock(self) -> Dict[str, int]:
        """Get current stock levels"""
        pass
    
    async def place_order(self, order_data) -> OrderConfirmation:
        """Submit completed order"""
        pass
    
    async def check_delivery_zones(self, address) -> bool:
        """Validate delivery zone"""
        pass

# adapters/client_db/rest_api.py
class RESTClientDB(ClientDatabaseBase):
    """Connect via REST API"""
    def __init__(self, api_endpoint, api_key):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
    
    async def get_menu(self):
        response = await self.client.get(
            f"{self.api_endpoint}/menu",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return Menu.from_json(response.json())

# adapters/client_db/sql_database.py
class SQLClientDB(ClientDatabaseBase):
    """Connect directly to SQL database"""
    def __init__(self, connection_string):
        self.db = Database(connection_string)
    
    async def get_menu(self):
        rows = await self.db.query("SELECT * FROM menu_items WHERE active=1")
        return Menu.from_rows(rows)

# adapters/client_db/factory.py
class ClientDBFactory:
    @staticmethod
    def create(db_type: str, config: Dict) -> ClientDatabaseBase:
        if db_type == "rest":
            return RESTClientDB(config["endpoint"], config["api_key"])
        elif db_type == "sql":
            return SQLClientDB(config["connection_string"])
        # ... more types
        else:
            raise ValueError(f"Unknown DB type: {db_type}")
```

---

### 7️⃣ STATE MANAGEMENT (Redis)

**Purpose:** Persistent session state across calls

```python
# system/state_manager.py
class StateManager:
    """Manage conversation state in Redis"""
    
    async def get_state(self, session_id):
        """Get state from Redis"""
        data = await self.redis.get(f"session:{session_id}")
        return ConversationState.from_json(data)
    
    async def save_state(self, session_id, state):
        """Save state to Redis with TTL"""
        await self.redis.setex(
            f"session:{session_id}",
            ttl=3600,  # 1 hour expiry
            value=state.to_json()
        )
```

---

## 📁 New Folder Structure

```
System Orchestration/
├── adapters/                          ← NEW
│   ├── __init__.py
│   ├── call_ingestion/
│   │   ├── __init__.py
│   │   ├── base.py                   ← Abstract class
│   │   ├── twilio.py                 ← Twilio wrapper
│   │   ├── custom_voip.py            ← VoIP wrapper
│   │   └── webrtc.py                 ← WebRTC wrapper
│   ├── stt_client.py                 ← STT (multi-provider)
│   ├── tts_client.py                 ← TTS (multi-provider)
│   ├── client_db/
│   │   ├── __init__.py
│   │   ├── base.py                   ← Abstract class
│   │   ├── rest_api.py               ← REST API wrapper
│   │   ├── sql_database.py           ← SQL wrapper
│   │   └── factory.py                ← Factory pattern
│   └── redis_client.py               ← Redis wrapper
├── audio/                             ← NEW
│   ├── __init__.py
│   ├── audio_gateway.py              ← Real-time audio handling
│   ├── audio_buffer.py               ← Buffering/jitter
│   └── codecs.py                     ← Audio codec handling
├── system/                            ← EXISTING (ENHANCED)
│   ├── audio_io.py                   ← ENHANCED: use AudioGateway
│   ├── conversation_manager.py       ← ENHANCED: add client_db param
│   ├── state_manager.py              ← NEW: session persistence
│   └── bootsrap.py                   ← ENHANCED: wire everything
├── handlers/                          ← EXISTING (ENHANCED)
│   └── order_handlers.py             ← ENHANCED: add client_db queries
├── docker-compose.yml                 ← UPDATED
├── Dockerfile                         ← UPDATED
├── requirements.txt                   ← UPDATED
└── config/
    ├── development.env
    ├── staging.env
    └── production.env
```

---

## 🚀 FastRTC vs Alternatives

### FastRTC Evaluation

| Aspect | FastRTC | Why Use | Why NOT Use |
|--------|---------|---------|-----------|
| **Purpose** | WebRTC library | Browser audio | Already have Twilio/VoIP |
| **Latency** | Low (~50ms) | ✅ Real-time | ❌ Can introduce extra complexity |
| **Use case** | Peer-to-peer | ✅ If browser-based | ❌ Old VoIP systems don't support |
| **Maintenance** | Community-driven | - | ⚠️ May need forking |

### **Recommendation: Hybrid Approach**

```
✅ USE FastRTC IF:
   - Building WebRTC browser interface for direct calls
   - Want peer-to-peer calling
   - Have modern infrastructure

❌ SKIP FastRTC IF:
   - Using Twilio (they handle WebRTC)
   - Using custom VoIP (handled by their protocol)
   - Want simplicity (use provider's native SDK)

💡 BEST APPROACH:
   1. Keep wrapper pattern (works with any protocol)
   2. Support FastRTC AS ONE OPTION
   3. Primary: Use provider-native SDKs
   4. Fallback: Custom RTP/WebSocket handler

Audio Transport OPTIONS:
- Twilio → WebSocket (Twilio Media Streams)
- Custom VoIP → RTP (standard)
- Browser → WebRTC (FastRTC or Native)
- All converge to common AudioGateway format
```

---

## 💾 Database Integration Examples

### Scenario 1: Intent triggers DB lookup

```python
# Intent: "Do you have pizza?"
# Handler needs to check real-time stock

class ViewMenuItemHandler:
    async def execute(self, nlu_result, state, client_db_accessor):
        item_name = nlu_result.entities.get("item_name")
        
        # Query client database for product details
        product = await client_db_accessor.get_product(item_name)
        
        if product and product.in_stock:
            return f"Yes, we have {item_name}! It costs ${product.price}"
        else:
            return f"Sorry, {item_name} is not available right now"
```

### Scenario 2: Order placement triggers DB insert

```python
# Intent: "Confirm order"
# Handler submits order to client system

class ConfirmOrderHandler:
    async def execute(self, nlu_result, state, client_db_accessor):
        order_data = {
            "items": state.slots["order_items"],
            "quantity": state.slots["quantity_per_item"],
            "delivery_type": state.slots["order_type"],
            "delivery_address": state.slots["delivery_address"]
        }
        
        # Submit to client's database
        order_id = await client_db_accessor.place_order(order_data)
        
        return f"Order confirmed! ID: {order_id}"
```

---

## 🐳 Docker Orchestration

### docker-compose.yml (Full Stack)

```yaml
version: '3.8'

services:
  
  # Main Application
  app:
    build: .
    container_name: breezi-orchestration
    ports:
      - "8000:8000"  # Main API
      - "8001:8001"  # Audio WebSocket
    environment:
      - CALL_INGESTION_TYPE=${CALL_INGESTION_TYPE}
      - STT_PROVIDER=${STT_PROVIDER}
      - TTS_PROVIDER=${TTS_PROVIDER}
      - CLIENT_DB_TYPE=${CLIENT_DB_TYPE}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    networks:
      - breezi-network

  # Redis (Session Storage)
  redis:
    image: redis:7-alpine
    container_name: breezi-redis
    ports:
      - "6379:6379"
    networks:
      - breezi-network

  # Optional: Vector DB (for similarity search)
  milvus:
    image: milvusdb/milvus:latest
    container_name: breezi-vectordb
    ports:
      - "19530:19530"
      - "9091:9091"
    environment:
      - COMMON_STORAGETYPE=local
    networks:
      - breezi-network

networks:
  breezi-network:
    driver: bridge
```

---

## 📊 Latency Budget Breakdown

```
Total Budget: 200ms

STT Processing:       75ms  (speech-to-text)
  └─ Network:        15ms
  └─ Streaming:      40ms
  └─ Processing:     20ms

System Orchestration: 30ms (NLU + Handlers)
  └─ NLU:            15ms
  └─ Handler logic:  10ms
  └─ DB query (opt): 5ms (can be async)

TTS Processing:       80ms (text-to-speech)
  └─ Network:        15ms
  └─ Synthesis:      50ms
  └─ Streaming:      15ms

Buffer/Network:       15ms  (jitter, routing)

─────────────────────────────
Total Latency:       200ms ✅
```

---

## 🔧 Implementation Roadmap

### PHASE 1: Audio Gateway (Days 1-2)
- [ ] Audio streaming gateway
- [ ] Support for audio chunking
- [ ] Jitter buffer implementation

### PHASE 2: Call Ingestion Wrappers (Days 3-5)
- [ ] Twilio adapter
- [ ] Custom VoIP adapter
- [ ] WebRTC adapter (optional)

### PHASE 3: STT/TTS Integration (Days 6-8)
- [ ] STT client (multi-provider)
- [ ] TTS client (multi-provider)
- [ ] Streaming support

### PHASE 4: Database Abstraction (Days 9-10)
- [ ] Base DB class
- [ ] REST API adapter
- [ ] SQL adapter
- [ ] Factory pattern

### PHASE 5: System Integration (Days 11-14)
- [ ] Update conversation manager
- [ ] Update handlers
- [ ] State persistence (Redis)
- [ ] Full E2E testing

### PHASE 6: Docker & Deployment (Days 15-20)
- [ ] Docker setup
- [ ] docker-compose orchestration
- [ ] Configuration management
- [ ] Production readiness

---

## ✅ Key Decisions Made

| Decision | Reasoning |
|----------|-----------|
| **Wrapper Pattern** | Supports multiple call sources without code duplication |
| **StreamingPipeline** | Enables real-time audio processing (not waiting for full files) |
| **Optional DB Queries** | Async to not block main conversation flow |
| **Redis State** | Fast session recovery, distributed deployment ready |
| **FastRTC Optional** | Keep flexibility - use what works for your call source |
| **Adapter Pattern** | Client DB type doesn't matter - abstracted away |
| **Docker Compose** | Local dev + staging - easily scales to K8s |

---

## 📝 Next Actions

1. **Confirm this architecture** ✓ (You approve?)
2. **Build Phase 1-2** → Audio Gateway + Call Ingestion
3. **Integrate with System Orchestration**
4. **Add STT/TTS**
5. **Test real-time latency**
6. **Containerize and deploy**

---

**Ready to start building?** 🚀
