"""
Interactive Test Mode - Test the system yourself!
Type any input and see how the system processes it
No scripts, no predefined test cases - YOU control the flow
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system
from utils.test_data_loader import TestDataLoader


def print_header():
    print("\n" + "="*80)
    print("🎮 INTERACTIVE TEST MODE - Test the System Yourself!")
    print("="*80)
    print("📌 Type any message and see how the system processes it")
    print("📌 System will detect language, classify intent, and execute handlers")
    print("📌 Type 'help' for available commands\n")


def print_help():
    print("\n" + "-"*80)
    print("📚 COMMANDS:")
    print("-"*80)
    print("  help          - Show this help message")
    print("  scenarios     - List all predefined test scenarios")
    print("  run <name>    - Run a predefined scenario (e.g., 'run pizza_order_incomplete')")
    print("  state         - Show current conversation state")
    print("  reset         - Reset conversation (start fresh)")
    print("  slots         - Show current slots")
    print("  fill <slot>=<value> - Manually fill a slot (e.g., 'fill order_type=delivery')")
    print("  exit          - Exit interactive mode")
    print("-"*80 + "\n")


def show_scenarios(loader):
    """Display all available test scenarios"""
    print("\n" + "-"*80)
    print("📋 AVAILABLE TEST SCENARIOS (from testdata.JSON):")
    print("-"*80)
    for i, name in enumerate(loader.scenario_names(), 1):
        scenario = loader.get_scenario(name)
        print(f"\n{i}. {name}")
        print(f"   Description: {scenario.get('description')}")
        print(f"   Test Input:  '{scenario.get('input')}'")
        print(f"   Expected Intent: {scenario.get('expected_intent')}")
    print("\n" + "-"*80 + "\n")


def run_predefined_scenario(scenario_name, loader, system, conversation, nlu):
    """Run a predefined scenario from testdata.JSON"""
    try:
        scenario = loader.get_scenario(scenario_name)
    except KeyError:
        print(f"❌ Scenario '{scenario_name}' not found!")
        return
    
    print(f"\n{'='*80}")
    print(f"🎬 RUNNING SCENARIO: {scenario.get('name')}")
    print(f"{'='*80}")
    print(f"📝 {scenario.get('description')}\n")
    
    user_input = scenario.get('input')
    slot_updates = scenario.get('slot_updates', {})
    
    # Process input
    print(f"🎤 INPUT: '{user_input}'")
    
    # NLU
    nlu_result = nlu.parse(user_input)
    print(f"\n🧠 NLU ANALYSIS:")
    print(f"   Intent: {nlu_result.intent}")
    print(f"   Entities: {nlu_result.entities}")
    print(f"   Language: {nlu_result.language}")
    
    # Conversation
    response = conversation.handle_message(user_input, session_id="interactive")
    print(f"\n💬 RESPONSE: {response}")
    
    # Check slots
    if conversation.state:
        missing = conversation.state.missing_slots()
        print(f"\n📊 SLOT STATUS:")
        print(f"   Filled Slots: {conversation.state.slots}")
        print(f"   Missing: {missing if missing else 'None ✅'}")
        
        # Apply configured slot updates
        if missing and slot_updates:
            print(f"\n📋 APPLYING CONFIGURED SLOT UPDATES:")
            for slot_name, slot_value in slot_updates.items():
                conversation.state.update_slot(slot_name, slot_value)
                print(f"   ✓ {slot_name} = '{slot_value}'")
            
            if not conversation.state.missing_slots():
                print(f"\n✅ All slots now filled!")


def process_user_input(user_input, conversation, nlu, system):
    """Process a user input through the full pipeline"""
    
    print(f"\n{'='*80}")
    print(f"🎤 YOU SAID: '{user_input}'")
    print(f"{'='*80}\n")
    
    # Step 1: NLU Analysis
    print("🧠 NLU ANALYSIS:")
    nlu_result = nlu.parse(user_input)
    print(f"   Intent: {nlu_result.intent}")
    print(f"   Entities: {nlu_result.entities}")
    print(f"   Language: {nlu_result.language}")
    
    # Step 2: Process through conversation manager
    print(f"\n💬 CONVERSATION PROCESSING:")
    response = conversation.handle_message(user_input, session_id="interactive")
    print(f"   Response: {response}")
    
    # Step 3: Show slot status
    if conversation.state:
        print(f"\n📊 CONVERSATION STATE:")
        print(f"   Intent: {conversation.state.intent}")
        print(f"   Filled Slots: {conversation.state.slots}")
        missing = conversation.state.missing_slots()
        if missing:
            print(f"   ⚠️  Missing Slots: {missing}")
            print(f"   💡 Tip: Use 'fill slot_name=value' to fill missing slots")
        else:
            print(f"   ✅ All slots filled!")
    
    print()


def show_state(conversation):
    """Display current conversation state"""
    if not conversation.state:
        print("\n❌ No active conversation state")
        return
    
    print(f"\n{'='*80}")
    print("📊 CURRENT CONVERSATION STATE")
    print(f"{'='*80}")
    print(f"Intent: {conversation.state.intent}")
    print(f"Slots: {conversation.state.slots}")
    missing = conversation.state.missing_slots()
    print(f"Missing Slots: {missing if missing else 'None ✅'}")
    print()


def fill_slot(slot_spec, conversation):
    """Fill a slot manually (e.g., 'order_type=delivery')"""
    try:
        slot_name, slot_value = slot_spec.split("=", 1)
        slot_name = slot_name.strip()
        slot_value = slot_value.strip()
        
        if not conversation.state:
            print("❌ No active conversation. Start with a user input first!")
            return
        
        conversation.state.update_slot(slot_name, slot_value)
        print(f"\n✅ Set {slot_name} = '{slot_value}'")
        
        missing = conversation.state.missing_slots()
        if missing:
            print(f"⚠️  Still missing: {missing}")
        else:
            print(f"✅ All slots filled!")
        print()
    except ValueError:
        print("❌ Invalid format! Use: fill slot_name=value")


def main():
    """Main interactive test loop"""
    
    # Initialize
    print_header()
    
    try:
        loader = TestDataLoader()
        print("✅ Test scenarios loaded")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return
    
    print("🔧 Building system...")
    system = build_system()
    conversation = system["conversation"]
    nlu = system["nlu"]
    print("✅ System ready!\n")
    
    # Interactive loop
    session_count = 0
    while True:
        try:
            user_input = input("💬 You> ").strip()
            
            if not user_input:
                continue
            
            # Commands
            if user_input.lower() == "exit":
                print("\n👋 Goodbye!")
                break
            
            elif user_input.lower() == "help":
                print_help()
            
            elif user_input.lower() == "scenarios":
                show_scenarios(loader)
            
            elif user_input.lower().startswith("run "):
                scenario_name = user_input[4:].strip()
                run_predefined_scenario(scenario_name, loader, system, conversation, nlu)
            
            elif user_input.lower() == "state":
                show_state(conversation)
            
            elif user_input.lower() == "reset":
                conversation.state = None
                print("✅ Conversation reset!\n")
            
            elif user_input.lower() == "slots":
                if conversation.state:
                    print(f"\n📋 Slots: {conversation.state.slots}\n")
                else:
                    print("❌ No active conversation\n")
            
            elif user_input.lower().startswith("fill "):
                slot_spec = user_input[5:].strip()
                fill_slot(slot_spec, conversation)
            
            else:
                # Regular user input
                session_count += 1
                process_user_input(user_input, conversation, nlu, system)
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
