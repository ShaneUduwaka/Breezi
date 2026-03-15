"""
Demonstration of Terminal Test Mode Flow
Shows how the slot-filling works without requiring interactive input
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system


def demonstrate_slot_filling():
    """Demonstrate the complete slot-filling flow"""

    print("\n" + "="*80)
    print("🎯 TERMINAL TEST MODE DEMONSTRATION")
    print("="*80)
    print("Flow: User Input → NLU → Check Slots → Fill Missing → Execute Handler")
    print()

    # Build system
    system = build_system()
    conversation = system["conversation"]
    nlu = system["nlu"]
    registry = system["registry"]
    rag = system.get("rag")
    ctx = system.get("context_memory")

    # prepopulate rag with a cached menu for demonstration
    if rag:
        rag.put("menu_overview", "📋 Cached menu from RAG store: burgers, fries, drinks.")


    # Test Case 1: Order pizza (requires slot filling)
    print("🧪 TEST CASE 1: Order Pizza (Missing Slots)")
    print("-" * 50)

    user_input = "I want to order a pizza"
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

        # Step 5: Simulate user providing slot values directly
        print("\n📝 Simulating user providing slot values:")
        conversation.state.update_slot("order_type", "delivery")
        print("   ✓ order_type = 'delivery'")
        conversation.state.update_slot("quantity_per_item", "2")
        print("   ✓ quantity_per_item = '2'")

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
    print("🧪 TEST CASE 2: Show Menu (Complete Request)")
    print("-" * 50)

    # Reset conversation
    conversation.state = None

    user_input = "show me the menu"
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
    print("• User input comes from terminal (no STT)")
    print("• NLU parses intent + entities")
    print("• DialogOrchestrator checks required slots")
    print("• If missing: Print LLM prompt, wait for direct slot values")
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