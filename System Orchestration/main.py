# main.py
"""
Main entry point for AI Call Agent System
Template-based configuration - all test data comes from testdata.JSON
"""

import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system
from utils.test_data_loader import TestDataLoader


def main():
    """
    Main entry point
    Demonstrates using configuration-driven test data instead of hardcoding
    """
    
    print("\n" + "="*70)
    print("🚀 BREEZI AI CALL AGENT - TEMPLATE-BASED MODE")
    print("="*70)
    print("Configuration: Loads ALL test data from testdata.JSON")
    print("No hardcoding in Python code - fully template-driven!\n")
    
    # Step 1: Load test configuration
    print("📋 Loading test scenarios from configuration...")
    try:
        loader = TestDataLoader()
        print("✅ Test scenarios loaded successfully!\n")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 2: Display available scenarios
    print("Available test scenarios:")
    for scenario_name in loader.scenario_names():
        desc = loader.get_description(scenario_name)
        print(f"  • {scenario_name}: {desc}")
    
    # Step 3: Get scenario to run
    default_scenario = loader.get_default_scenario()
    print(f"\n🎯 Running default scenario: '{default_scenario}'")
    
    # Step 4: Build system
    print("\n🔧 Building system...")
    system = build_system()
    conversation = system["conversation"]
    nlu = system["nlu"]
    print("✅ System built successfully!\n")
    
    # Step 5: Load and execute scenario
    scenario = loader.get_scenario(default_scenario)
    user_input = loader.get_input(default_scenario)
    slot_updates = loader.get_slot_updates(default_scenario)
    expected_intent = loader.get_expected_intent(default_scenario)
    
    print("="*70)
    print(f"SCENARIO: {scenario.get('name')}")
    print("="*70)
    print(f"📝 Description: {scenario.get('description')}")
    print(f"🎤 User Input: '{user_input}'")
    print(f"🎯 Expected Intent: {expected_intent}\n")
    
    # Step 6: Process through NLU
    print("→ Processing through NLU...")
    nlu_result = nlu.parse(user_input)
    print(f"✓ Intent: {nlu_result.intent}")
    print(f"✓ Entities: {nlu_result.entities}\n")
    
    # Step 7: Handle through conversation manager
    print("→ Processing through Conversation Manager...")
    response = conversation.handle_message(user_input, session_id="main-demo")
    print(f"✓ Response: {response}\n")
    
    # Step 8: Fill missing slots (if any) using configured values
    if slot_updates:
        print("→ Filling missing slots with configured values...")
        for slot_name, slot_value in slot_updates.items():
            conversation.state.update_slot(slot_name, slot_value)
            print(f"✓ {slot_name} = '{slot_value}'")
        print()
    
    # Step 9: Check final state
    if conversation.state:
        print("📊 Final Conversation State:")
        print(f"✓ Intent: {conversation.state.intent}")
        print(f"✓ Slots: {conversation.state.slots}")
        missing = conversation.state.missing_slots()
        if missing:
            print(f"✓ Missing slots: {missing}")
        else:
            print("✓ All slots filled! ✅")
    
    print("\n" + "="*70)
    print("✅ Configuration-driven execution completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()



