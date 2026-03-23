"""
Demonstration of Terminal Test Mode Flow with Configuration-Driven Data
Shows how the slot-filling works using testdata.JSON - NO HARDCODING!
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system
from utils.test_data_loader import MockDataLoader


def demonstrate_slot_filling():
    """Demonstrate the complete slot-filling flow with configuration-driven data"""

    print("\n" + "="*80)
    print("🎯 TERMINAL TEST MODE DEMONSTRATION - CONFIGURATION-DRIVEN")
    print("="*80)
    print("Flow: User Input → NLU → Check Slots → Fill Missing → Execute Handler")
    print("All test data loaded from testdata.JSON - No hardcoding!\n")

    # Load test configuration
    try:
        loader = MockDataLoader()
        print("✅ Test scenarios loaded from testdata.JSON\n")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return

    # Build system
    print("🔧 Building system...")
    system = build_system()
    conversation = system["conversation"]
    nlu = system["nlu"]
    registry = system["registry"]
    rag = system.get("rag")
    ctx = system.get("context_memory")
    print("✅ System built successfully!\n")

    # prepopulate rag with a cached menu for demonstration
    if rag:
        rag.put("menu_overview", "📋 Cached menu from RAG store: burgers, fries, drinks.")

    # Test Case 1: Load from configuration
    print("🧪 TEST CASE 1: Order Pizza (from testdata.JSON)")
    print("-" * 50)

    scenario_name = "pizza_order_incomplete"
    scenario = loader.get_scenario(scenario_name)
    user_input = loader.get_input(scenario_name)
    slot_updates = loader.get_slot_updates(scenario_name)
    
    print(f"📝 Scenario: {scenario.get('description')}")
    print(f"🎤 User Input: '{user_input}'")

    # Step 1: NLU parsing
    nlu_result = nlu.parse(user_input)
    print(f"🧠 NLU Result: intent='{nlu_result.intent}', entities={nlu_result.entities}")

    # Step 2: Process through conversation manager (session id attached)
    response = conversation.handle_message(user_input, session_id="demo-session")
    print(f"💬 Initial Response: {response}")

    # Step 3: Check for missing slots
    if conversation.state and conversation.state.missing_slots():
        missing = conversation.state.missing_slots()
        print(f"❓ Missing Slots: {missing}")

        # Step 4: Show LLM prompt that would be generated
        print("💬 LLM Prompt that would be generated:")
        print("   'Please provide the required information.'")
        print(f"   Missing: {missing}")

        # Step 5: Apply configured slot updates (no hardcoding!)
        print("\n📋 Applying configured slot updates from testdata.JSON:")
        for slot_name, slot_value in slot_updates.items():
            conversation.state.update_slot(slot_name, slot_value)
            print(f"   ✓ {slot_name} = '{slot_value}'")

        # Step 6: Check if all slots filled
        if not conversation.state.missing_slots():
            print("\n✅ All slots filled! Current state:")
            print(f"   Intent: {conversation.state.intent}")
            print(f"   Slots: {conversation.state.slots}")

            # Step 7: Ask for confirmation before executing
            print("⚡ Ready to execute handler. Confirm? (simulated: yes)")

            # Step 8: Execute handler
            handler = registry.get_handler(conversation.state.intent)
            if handler:
                result = handler(conversation.state)
                print(f"✅ Handler Result: {result}")
            else:
                print("❌ No handler found")

    print("\n" + "-"*80)

    # Test Case 2: Complete request (no slot filling needed)
    print("🧪 TEST CASE 2: Show Menu (from testdata.JSON)")
    print("-" * 50)

    # Reset conversation
    conversation.state = None

    scenario_name = "show_menu"
    scenario = loader.get_scenario(scenario_name)
    user_input = loader.get_input(scenario_name)
    
    print(f"📝 Scenario: {scenario.get('description')}")
    print(f"🎤 User Input: '{user_input}'")

    nlu_result = nlu.parse(user_input)
    print(f"🧠 NLU Result: intent='{nlu_result.intent}', entities={nlu_result.entities}")

    response = conversation.handle_message(user_input, session_id="demo-session")
    print(f"💬 Response: {response}")

    if conversation.state:
        missing = conversation.state.missing_slots()
        if missing:
            print(f"❓ Missing: {missing}")
        else:
            print("✅ No missing slots - executed immediately")

    print("\n" + "="*80)
    print("✓ Demonstration completed!")
    print("\n📋 SUMMARY:")
    print("• All test data loaded from testdata.JSON - NO HARDCODING!")
    print("• User input comes from configuration")
    print("• Slot updates come from configuration")
    print("• NLU parses intent + entities")
    print("• DialogOrchestrator checks required slots")
    print("• If missing: Apply configured slot values")
    print("• If complete: Ask confirmation, then execute handler")
    print("• Conversation state maintained across inputs")

    # show stored context if available
    if ctx and conversation.session_id:
        print("\n📂 Stored turns for session:")
        turns = ctx.get_turns(conversation.session_id)
        for t in turns:
            print(t)


if __name__ == "__main__":
    demonstrate_slot_filling()