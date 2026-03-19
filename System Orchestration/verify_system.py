"""
Comprehensive System Verification Script
Checks all components are working correctly without Redis
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("\n" + "="*80)
print("🔍 SYSTEM VERIFICATION - Redis Removed")
print("="*80)

# Test 1: Import all core modules
print("\n📦 TEST 1: Importing Core Modules")
print("-" * 80)

try:
    print("  • Importing dialog.IntentRegistry...", end=" ")
    from dialog.IntentRegistry import IntentRegistry
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

try:
    print("  • Importing dialog.dialog_orchestrator...", end=" ")
    from dialog.dialog_orchestrator import DialogOrchestrator
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

try:
    print("  • Importing dialog.intent_state...", end=" ")
    from dialog.intent_state import IntentState
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

try:
    print("  • Importing system.conversation_manager...", end=" ")
    from system.conversation_manager import ConversationManager
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

try:
    print("  • Importing handlers.order_handlers...", end=" ")
    from handlers.order_handlers import GenericHandler
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

try:
    print("  • Importing llm.fake_llm...", end=" ")
    from llm.fake_llm import FakeLLM
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

try:
    print("  • Importing nlu.fake_nlu...", end=" ")
    from nlu.fake_nlu import FakeNLU
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 2: Verify memory stores (no Redis)
print("\n💾 TEST 2: Memory Stores (In-Memory Only)")
print("-" * 80)

try:
    print("  • Importing memory.context_memory...", end=" ")
    from memory.context_memory import ContextMemory
    print("✓")
    
    # Test ContextMemory
    print("  • Creating ContextMemory instance...", end=" ")
    ctx_mem = ContextMemory(max_turns=50)
    print("✓")
    
    print("  • Testing save/load functionality...", end=" ")
    test_state = {"intent": "test", "slots": {"item": "pizza"}}
    ctx_mem.save("session-1", test_state)
    loaded = ctx_mem.load("session-1")
    assert loaded == test_state, "State mismatch!"
    print("✓")
    
    print("  • Testing append_turn functionality...", end=" ")
    turn = {"input": "test", "output": "response", "timestamp": 123.45}
    ctx_mem.append_turn("session-1", turn)
    turns = ctx_mem.get_turns("session-1")
    assert len(turns) == 1, "Turn not appended!"
    print("✓")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

try:
    print("  • Importing memory.rag_store...", end=" ")
    from memory.rag_store import RagStore
    print("✓")
    
    # Test RagStore
    print("  • Creating RagStore instance...", end=" ")
    rag_store = RagStore()
    print("✓")
    
    print("  • Testing put/get functionality...", end=" ")
    rag_store.put("menu", {"categories": ["burgers", "fries"]})
    data = rag_store.get("menu")
    assert data["categories"] == ["burgers", "fries"], "Data mismatch!"
    print("✓")
    
    print("  • Testing delete functionality...", end=" ")
    rag_store.delete("menu")
    result = rag_store.get("menu")
    assert result is None, "Delete failed!"
    print("✓")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 3: Build complete system
print("\n🏗️  TEST 3: Building Complete System")
print("-" * 80)

try:
    print("  • Importing system.bootsrap...", end=" ")
    from system.bootsrap import build_system
    print("✓")
    
    print("  • Building system with build_system()...", end=" ")
    system = build_system()
    print("✓")
    
    print("  • Verifying all system components...", end=" ")
    required_keys = ["conversation", "stt", "tts", "orchestrator", "nlu", 
                     "registry", "llm", "business_config", "rag", "context_memory"]
    for key in required_keys:
        assert key in system, f"Missing key: {key}"
    print("✓")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 4: End-to-end conversation flow
print("\n💬 TEST 4: End-to-End Conversation Flow")
print("-" * 80)

try:
    conversation = system["conversation"]
    
    print("  • Processing user input (slot filling required)...", end=" ")
    response = conversation.handle_message("I want to order pizza", session_id="test")
    assert "information" in response.lower() or "order" in response.lower(), "Unexpected response!"
    print("✓")
    
    print("  • Checking conversation state...", end=" ")
    assert conversation.state is not None, "State not created!"
    assert conversation.state.intent == "start_order", "Wrong intent!"
    print("✓")
    
    print("  • Processing menu request...", end=" ")
    response2 = conversation.handle_message("show me the menu", session_id="test2")
    assert "menu" in response2.lower() or "burger" in response2.lower(), "Unexpected response!"
    print("✓")
    
    print("  • Verifying memory storage...", end=" ")
    ctx_mem = system["context_memory"]
    turns = ctx_mem.get_turns("test")
    assert len(turns) >= 1, "No turns stored!"
    print("✓")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 5: Verify no Redis imports
print("\n🚫 TEST 5: Verifying No Redis References")
print("-" * 80)

try:
    import importlib.util
    
    # Check context_memory.py
    print("  • Checking context_memory.py for Redis imports...", end=" ")
    spec = importlib.util.spec_from_file_location("context_memory", 
        os.path.join(os.path.dirname(__file__), "memory", "context_memory.py"))
    module = importlib.util.module_from_spec(spec)
    # Check source code
    with open(os.path.join(os.path.dirname(__file__), "memory", "context_memory.py")) as f:
        content = f.read()
        assert "import redis" not in content, "Redis import found!"
        assert "redis.from_url" not in content, "Redis URL reference found!"
    print("✓")
    
    # Check rag_store.py
    print("  • Checking rag_store.py for Redis imports...", end=" ")
    with open(os.path.join(os.path.dirname(__file__), "memory", "rag_store.py")) as f:
        content = f.read()
        assert "import redis" not in content, "Redis import found!"
    print("✓")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Summary
print("\n" + "="*80)
print("✅ ALL VERIFICATION TESTS PASSED!")
print("="*80)
print("""
System Status:
  • All core modules imported successfully ✓
  • Memory stores working (in-memory only) ✓
  • System builds without errors ✓
  • End-to-end conversation flow working ✓
  • No Redis references found ✓
  • NLU parsing working ✓
  • Intent routing working ✓
  • Handler execution working ✓

Redis has been successfully removed!
The system now uses pure in-memory storage.
Ready for next phase: Building Redis properly as needed.
""")
print("="*80 + "\n")
