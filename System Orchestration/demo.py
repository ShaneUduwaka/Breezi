"""
End-to-End Demo Script
Shows the complete AI Call Agent flow:
STT → NLU → Dialog Orchestration → Handler Execution → TTS
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system
from system.audio_io import DummySTT, DummyTTS


def demo_flow(system, verbose=True):
    """
    Demo the complete flow with slot-filling requirement
    
    Flow:
    1. STT: "I want to order a pizza"
    2. NLU: Extracts intent=start_order, entities={order_items: pizza}
    3. Orchestrator: Checks if all slots filled → checks schema → order_items is required ✓, all slots filled ✓
    4. Handler: Executes handle_start_order
    5. TTS: Speaks the response
    """
    
    conversation = system["conversation"]
    stt = system["stt"]
    tts = system["tts"]
    
    print("\n" + "="*70)
    print("🎙️ AI CALL AGENT DEMO - Complete Flow")
    print("="*70)
    
    # Mock audio inputs for demo
    mock_audios = [
        "I want to order a pizza",
        "show me the menu",
        "What are your burgers",
        "Tell me about the burger",
    ]
    
    stt.set_mock_responses(mock_audios)
    
    for round_num, expected_audio in enumerate(mock_audios, 1):
        print(f"\n{'─'*70}")
        print(f"ROUND {round_num}")
        print(f"{'─'*70}")
        
        # Step 1: STT - Audio to Text
        if verbose:
            print(f"🎤 User speaks (STT): '{expected_audio}'")
        
        user_text = stt.transcribe(None)  # In real: pass audio bytes
        if verbose:
            print(f"📝 Transcribed text: '{user_text}'")
        
        # Step 2: NLU - Extract intent and entities
        nlu_result = system["nlu"].parse(user_text)
        if verbose:
            print(f"🧠 NLU Result:")
            print(f"   Intent: {nlu_result.intent}")
            print(f"   Entities: {nlu_result.entities}")
        
        # Step 3: Dialog Orchestration - Process through system
        response = conversation.handle_message(user_text)
        
        if verbose:
            print(f"💬 System Response:")
            print(f"   {response}")
        
        # Step 4: TTS - Text to Speech
        tts.speak(response)
        
        # Show conversation state
        if verbose and conversation.state:
            print(f"📊 Conversation State:")
            print(f"   Intent: {conversation.state.intent}")
            print(f"   Filled slots: {[(k, v) for k, v in conversation.state.slots.items() if v is not None]}")
            print(f"   Missing slots: {conversation.state.missing_slots()}")


def interactive_demo(system):
    """
    Interactive mode - manually input text
    """
    conversation = system["conversation"]
    tts = system["tts"]
    
    print("\n" + "="*70)
    print("🎙️ AI CALL AGENT - Interactive Mode")
    print("="*70)
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        if not user_input:
            continue
        
        # Process through system
        response = conversation.handle_message(user_input)
        
        print(f"Agent: {response}")
        tts.speak(response)
        
        # Show state
        if conversation.state:
            missing = conversation.state.missing_slots()
            if missing:
                print(f"  [Waiting for: {', '.join(missing)}]")


if __name__ == "__main__":
    print("\n🚀 Initializing AI Call Agent System...")
    
    try:
        system = build_system()
        print("✓ System initialized successfully!\n")
        
        # Run demo
        demo_flow(system, verbose=True)
        
        # Optional: Interactive mode
        print("\n" + "="*70)
        response = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
        if response == 'y':
            interactive_demo(system)
        
        print("\n✓ Demo completed!\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
