"""
Automated Test Script for Terminal Mode
Demonstrates the slot-filling flow with configuration-driven test data
All test inputs and expected values come from testdata.JSON - NO HARDCODING!
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system
from utils.test_data_loader import TestDataLoader


def run_test_scenario(scenario_name, loader, system):
    """
    Run a single test scenario using configuration from testdata.JSON
    
    Args:
        scenario_name: Name of scenario to run
        loader: TestDataLoader instance
        system: Built system from build_system()
    """
    scenario = loader.get_scenario(scenario_name)
    user_input = loader.get_input(scenario_name)
    slot_updates = loader.get_slot_updates(scenario_name)
    expected_intent = loader.get_expected_intent(scenario_name)
    
    conversation = system["conversation"]
    nlu = system["nlu"]
    
    print(f"\n🧪 TEST: {scenario.get('name')}")
    print("-" * 60)
    print(f"📝 {scenario.get('description')}")
    print(f"🎤 User Input: '{user_input}'")
    print(f"🎯 Expected Intent: {expected_intent}\n")
    
    # Step 1: NLU parsing
    nlu_result = nlu.parse(user_input)
    print(f"✓ NLU Result: intent='{nlu_result.intent}', entities={nlu_result.entities}")
    
    # Step 2: Process through conversation manager
    response = conversation.handle_message(user_input, session_id=f"test-{scenario_name}")
    print(f"✓ Response: {response}")
    
    # Step 3: Check missing slots and apply configured updates
    if conversation.state and conversation.state.missing_slots():
        missing = conversation.state.missing_slots()
        print(f"❓ Missing slots: {missing}")
        
        # Apply slot updates from configuration
        if slot_updates:
            print("\n📋 Applying configured slot updates:")
            for slot_name, slot_value in slot_updates.items():
                conversation.state.update_slot(slot_name, slot_value)
                print(f"   ✓ {slot_name} = '{slot_value}'")
            print()
        
        # Check if all slots filled now
        if not conversation.state.missing_slots():
            print("✅ All slots filled! Ready to execute.")
            print(f"📊 Final state:")
            print(f"   Intent: {conversation.state.intent}")
            print(f"   Slots: {conversation.state.slots}")
            
            # Execute handler if available
            handler = system["conversation"].registry.get_handler(conversation.state.intent)
            if handler:
                result = handler(conversation.state)
                print(f"✓ Handler Result: {result}")
    else:
        print("✅ No missing slots - executed immediately")
        if conversation.state:
            print(f"📊 State:")
            print(f"   Intent: {conversation.state.intent}")
            print(f"   Slots: {conversation.state.slots}")


def main():
    """Main test runner - uses configuration-driven approach"""
    
    print("\n" + "="*70)
    print("🧪 SLOT FILLING TESTS - CONFIGURATION-DRIVEN")
    print("="*70)
    print("All test data loaded from testdata.JSON - No hardcoding!\n")
    
    # Step 1: Load test configuration
    try:
        loader = TestDataLoader()
        print("✅ Test scenarios loaded from testdata.JSON\n")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 2: Build system
    print("🔧 Building system...")
    system = build_system()
    print("✅ System built successfully!\n")
    
    # Step 3: Run configured test scenarios
    test_scenarios = [
        "pizza_order_incomplete",
        "show_menu",
    ]
    
    for scenario_name in test_scenarios:
        if scenario_name in loader.scenario_names():
            run_test_scenario(scenario_name, loader, system)
    
    print("\n" + "="*70)
    print("✓ Configuration-driven slot filling tests completed!")
    print("="*70)


if __name__ == "__main__":
    main()