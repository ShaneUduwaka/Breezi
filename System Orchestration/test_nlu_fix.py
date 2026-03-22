#!/usr/bin/env python3
"""
Quick test for NLU intent classification fix
Tests that cancel_order, modify_order, and track_order are properly classified
"""

import sys
import json
sys.path.insert(0, '.')

from system.bootsrap import build_system

# Load config
with open('Business input/intent.JSON', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Build system
system = build_system()
nlu = system['nlu']

print('\n' + '='*80)
print('🧪 NLU INTENT CLASSIFICATION TEST')
print('='*80)

# Test cases
test_cases = [
    ('I want to order a pizza', 'start_order'),
    ('I want to cancel my previous order', 'cancel_order'),
    ('Cancel that order', 'cancel_order'),
    ('Can you modify my order', 'modify_order'),
    ('Where is my order', 'track_order'),
    ('Can I have pizza', 'start_order'),
    ('I would like to place a new order', 'start_order'),
    ('Never mind, cancel it', 'cancel_order'),
    ('Change my order please', 'modify_order'),
    ('Check the status of my order', 'track_order'),
]

print('\nTesting intent classification:\n')
passed = 0
failed = 0

for text, expected_intent in test_cases:
    result = nlu.parse(text)
    actual_intent = result.intent
    status = '✅' if actual_intent == expected_intent else '❌'
    
    print(f'{status} Input: "{text}"')
    print(f'   Expected: {expected_intent}')
    print(f'   Actual: {actual_intent}')
    
    if actual_intent == expected_intent:
        passed += 1
    else:
        failed += 1
    print()

print('='*80)
print(f'📊 TEST RESULTS: {passed} passed, {failed} failed')
print('='*80 + '\n')

if failed == 0:
    print('✅ ALL TESTS PASSED - Intent classification is fixed!\n')
else:
    print(f'❌ {failed} tests failed - Review keyword configuration\n')
