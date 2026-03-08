"""
Simplified Terminal Test for AI Call Agent
- Takes user input from terminal (no STT)
- Skips LLM and TTS
- When slots missing: prints LLM prompt, expects user to provide slot values directly
- Maintains conversation state across inputs
- Asks for confirmation before executing handlers
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system


def print_conversation_state(conversation):
    """Print current conversation state"""
    if conversation.state:
        print(f"\n📊 Current State:")
        print(f"   Intent: {conversation.state.intent}")
        print(f"   Filled slots: {[(k, v) for k, v in conversation.state.slots.items() if v is not None]}")
        missing = conversation.state.missing_slots()
        if missing:
            print(f"   Missing slots: {missing}")
        else:
            print("   All slots filled ✓")


def handle_slot_filling(conversation, missing_slots):
    """Handle slot filling by asking user directly for missing values"""

    print(f"\n❓ Missing information needed: {', '.join(missing_slots)}")
    print("💬 LLM Prompt that would be generated:")
    print("   'Please provide the required information.'")
    print(f"   Missing: {missing_slots}")

    # Ask user to provide slot values directly
    print(f"\n📝 Please provide values for missing slots:")

    for slot_name in missing_slots:
        # Get slot definition for prompt
        intent_def = conversation.registry.get_intent(conversation.state.intent)
        slot_def = intent_def.get("slots", {}).get(slot_name, {})
        prompt = slot_def.get("prompt", f"Please provide {slot_name}")

        value = input(f"   {slot_name}: ").strip()
        if value:
            conversation.state.update_slot(slot_name, value)
            print(f"   ✓ Set {slot_name} = '{value}'")

    return conversation.state.missing_slots()


def terminal_test(system):
    """Main terminal testing loop"""

    conversation = system["conversation"]
    nlu = system["nlu"]

    print("\n" + "="*70)
    print("🧪 AI CALL AGENT - TERMINAL TEST MODE")
    print("="*70)
    print("Type 'quit' to exit, 'reset' to start new conversation")
    print("When slots are missing, provide values directly\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'reset':
            conversation.state = None
            print("🔄 Conversation reset")
            continue
        elif not user_input:
            continue

        print(f"\n🎤 Input: '{user_input}'")

        # Step 1: NLU parsing
        nlu_result = nlu.parse(user_input)
        print(f"🧠 NLU Result:")
        print(f"   Intent: {nlu_result.intent}")
        print(f"   Entities: {nlu_result.entities}")

        # Step 2: Process through conversation manager
        response = conversation.handle_message(user_input)

        # Step 3: Check if slots are missing
        if conversation.state and conversation.state.missing_slots():
            missing = handle_slot_filling(conversation, conversation.state.missing_slots())

            if not missing:
                # All slots now filled - ask for confirmation before executing
                print_conversation_state(conversation)
                confirm = input(f"\n⚡ Ready to execute '{conversation.state.intent}'. Proceed? (y/n): ").strip().lower()

                if confirm == 'y':
                    # Execute the handler
                    handler = conversation.registry.get_handler(conversation.state.intent)
                    if handler:
                        result = handler(conversation.state)
                        print(f"\n✅ Handler Result: {result}")
                    else:
                        print(f"\n❌ No handler found for {conversation.state.intent}")
                else:
                    print("⏸️ Execution cancelled")
        else:
            # No missing slots - this was a complete request
            print(f"\n💬 Response: {response}")
            print_conversation_state(conversation)


if __name__ == "__main__":
    print("\n🚀 Initializing Terminal Test System...")

    try:
        system = build_system()
        print("✓ System initialized successfully!\n")

        terminal_test(system)

        print("\n✓ Terminal test completed!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()