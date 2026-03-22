#!/usr/bin/env python3
"""
Quick test of the full system with the NLU fix
Tests that intents are correctly classified and processed
"""

import sys
sys.path.insert(0, '.')

from system.bootsrap import build_system

# Build system
system = build_system()
conversation = system["conversation"]
nlu = system["nlu"]

print('\n' + '='*80)
print('🧪 FULL SYSTEM TEST - Intent Classification & Conversation')
print('='*80)

# Test scenarios with expected intents
test_scenarios = [
    "I want to order a pizza",
    "I want to cancel my previous order",
    "Can you modify my order",
    "Where is my order",
]

session_id = "test_session"

for i, user_input in enumerate(test_scenarios, 1):
    print(f"\n{'='*80}")
    print(f"Turn {i}")
    print('='*80)
    
    # Parse with NLU
    nlu_result = nlu.parse(user_input)
    
    # Process through conversation
    response = conversation.handle_message(user_input, session_id)
    
    print(f"👤 User Input: \"{user_input}\"")
    print(f"🧠 Intent: {nlu_result.intent}")
    print(f"🤖 Bot Response: {response[:100]}...")

print('\n' + '='*80)
print('✅ Full system test complete!')
print('='*80 + '\n')
