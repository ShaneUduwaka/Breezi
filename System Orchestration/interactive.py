# interactive.py
"""
Interactive mode for testing the AI Call Agent System
Test multi-turn conversations with real-time user input
Supports English, Sinhala, and mixed language input
"""

import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system


def main():
    """
    Interactive conversation mode
    """
    
    print("\n" + "="*70)
    print("🚀 BREEZI AI CALL AGENT - INTERACTIVE MODE")
    print("="*70)
    print("💬 Have a real-time conversation with the system")
    print("📝 Supports English, Sinhala, and mixed language input")
    print("📌 Commands: 'state' (view conversation state), 'exit' (quit)")
    print("="*70 + "\n")
    
    # Build system
    print("🔧 Initializing system...")
    try:
        system = build_system()
        conversation = system["conversation"]
        nlu = system["nlu"]
        print("✅ System ready!\n")
    except Exception as e:
        print(f"❌ Error initializing system: {e}")
        return
    
    session_id = "interactive-session"
    turn_count = 0
    
    print("-" * 70)
    print("START CONVERSATION")
    print("-" * 70)
    print("Try saying things like:")
    print("  • 'I want to order a pizza'")
    print("  • 'delivery, 2 pieces'")
    print("  • 'පීසා එකක් order කරන්න' (Sinhala)")
    print("  • 'delivery එකක්' (Sinhala)")
    print("-" * 70 + "\n")
    
    while True:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()
            
            if not user_input:
                print("⚠️  Please enter something...\n")
                continue
            
            # Handle special commands
            if user_input.lower() == 'exit':
                print("\n👋 Goodbye!")
                break
            
            if user_input.lower() == 'state':
                print_conversation_state(conversation)
                continue
            
            turn_count += 1
            
            print(f"\n🔄 Turn {turn_count}:")
            print(f"📥 Input: '{user_input}'")
            
            # Process through NLU
            print("├─ 🧠 NLU Analysis:")
            nlu_result = nlu.parse(user_input)
            print(f"│  ├─ Intent: {nlu_result.intent}")
            print(f"│  └─ Entities: {nlu_result.entities if nlu_result.entities else '(none)'}")
            
            # Process through conversation manager
            print("├─ 💬 Conversation Manager:")
            response = conversation.handle_message(user_input, session_id=session_id)
            print(f"│  └─ Response: {response}")
            
            # Show current state
            print("├─ 📊 Current State:")
            if conversation.state:
                print(f"│  ├─ Intent: {conversation.state.intent}")
                print(f"│  ├─ Slots: {conversation.state.slots}")
                missing = conversation.state.missing_slots()
                if missing:
                    print(f"│  ├─ ⏳ Missing slots: {missing}")
                    print(f"│  └─ Status: Waiting for input...")
                else:
                    print(f"│  └─ ✅ All slots filled! Ready to execute.")
            else:
                print(f"│  └─ (No active state)")
            
            print("\n" + "-" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            print("-" * 70 + "\n")


def print_conversation_state(conversation):
    """
    Display full conversation state
    """
    print("\n" + "="*70)
    print("📊 CONVERSATION STATE")
    print("="*70)
    
    if conversation.state:
        print(f"Intent: {conversation.state.intent}")
        print(f"Slots: {conversation.state.slots}")
        missing = conversation.state.missing_slots()
        if missing:
            print(f"Missing: {missing}")
        else:
            print("Status: ✅ Complete - ready to execute!")
    else:
        print("No active conversation state")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
