"""
Automated Test Script for Terminal Mode
Demonstrates the slot-filling flow with pre-defined inputs
"""

import sys
import os
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dialog.IntentRegistry import IntentRegistry
from dialog.dialog_orchestrator import DialogOrchestrator
from system.conversation_manager import ConversationManager

from handlers.handler_mapping import HANDLERS
from llm.fake_llm import FakeLLM
from nlu.fake_nlu import FakeNLU


def build_system():
    """Build the simplified system for terminal testing"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "Business input", "intent.JSON")
    json_path = os.path.abspath(json_path)

    registry = IntentRegistry(json_path, handler_mapping=HANDLERS)
    llm = FakeLLM()
    orchestrator = DialogOrchestrator(registry, llm)
    nlu = FakeNLU()
    conversation = ConversationManager(registry, orchestrator, nlu)

    return {
        "conversation": conversation,
        "orchestrator": orchestrator,
        "nlu": nlu,
        "registry": registry,
        "llm": llm,
    }


def simulate_slot_filling_test():
    """Test the slot filling flow with simulated user inputs"""

    system = build_system()
    conversation = system["conversation"]

    print("\n" + "="*70)
    print("🧪 SLOT FILLING TEST - SIMULATED")
    print("="*70)

    # Test Case 1: Order pizza (missing slots)
    print("\n🧪 TEST 1: Order pizza (missing slots)")
    print("-" * 40)

    user_input = "I want to order a pizza"
    print(f"🎤 User: '{user_input}'")

    # NLU parsing
    nlu_result = system["nlu"].parse(user_input)
    print(f"🧠 NLU: intent='{nlu_result.intent}', entities={nlu_result.entities}")

    # Process through conversation
    response = conversation.handle_message(user_input)
    print(f"💬 Initial response: {response}")

    # Check missing slots
    if conversation.state and conversation.state.missing_slots():
        missing = conversation.state.missing_slots()
        print(f"❓ Missing slots: {missing}")

        print("💬 LLM Prompt would be:")
        print("   'Please provide the required information.'")
        print(f"   Missing: {missing}")

        # Simulate user providing slot values
        print("\n📝 Simulating user providing slot values:")
        conversation.state.update_slot("order_type", "delivery")
        print("   ✓ Set order_type = 'delivery'")
        conversation.state.update_slot("quantity_per_item", "2")
        print("   ✓ Set quantity_per_item = '2'")

        # Check if all slots filled
        if not conversation.state.missing_slots():
            print("\n✅ All slots filled! Ready to execute.")
            print("📊 Final state:")
            print(f"   Intent: {conversation.state.intent}")
            print(f"   Slots: {conversation.state.slots}")

            # Ask for confirmation (simulated)
            confirm = "y"  # Simulate user saying yes
            print(f"⚡ Execute? (simulated: {confirm})")

            if confirm == 'y':
                handler = conversation.registry.get_handler(conversation.state.intent)
                if handler:
                    result = handler(conversation.state)
                    print(f"✅ Handler Result: {result}")
                else:
                    print("❌ No handler found")

    # Test Case 2: Complete request (no missing slots)
    print("\n\n🧪 TEST 2: Show menu (complete request)")
    print("-" * 40)

    conversation.state = None  # Reset conversation
    user_input = "show me the menu"
    print(f"🎤 User: '{user_input}'")

    nlu_result = system["nlu"].parse(user_input)
    print(f"🧠 NLU: intent='{nlu_result.intent}', entities={nlu_result.entities}")

    response = conversation.handle_message(user_input)
    print(f"💬 Response: {response}")

    if conversation.state:
        missing = conversation.state.missing_slots()
        if missing:
            print(f"❓ Missing: {missing}")
        else:
            print("✅ No missing slots - executed immediately")

    print("\n" + "="*70)
    print("✓ Slot filling test completed!")


if __name__ == "__main__":
    simulate_slot_filling_test()