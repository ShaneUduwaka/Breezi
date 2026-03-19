"""
Test multi-turn conversation with NLU extraction
Verify if NLU extracts slot values from natural language across all turns
"""

from system.bootsrap import build_system

system = build_system()
conversation = system["conversation"]
nlu = system["nlu"]

print("\n" + "="*70)
print("🧪 TESTING MULTI-TURN CONVERSATION WITH NLU")
print("="*70)

# Round 1
print("\n🔵 ROUND 1: User orders pizza")
print("-"*70)
input1 = "I want to order a pizza"
print(f"User: {input1}")
nlu_result = nlu.parse(input1)
print(f"NLU: intent={nlu_result.intent}, entities={nlu_result.entities}, language={nlu_result.language}")
response1 = conversation.handle_message(input1, session_id="test")
print(f"Response: {response1}")
if conversation.state:
    print(f"State slots: {conversation.state.slots}")
    print(f"Missing: {conversation.state.missing_slots()}")

# Round 2 - User provides slot values naturally
print("\n🔵 ROUND 2: User provides missing info naturally")
print("-"*70)
input2 = "delivery, 2 pieces"
print(f"User: {input2}")
nlu_result = nlu.parse(input2)
print(f"NLU: intent={nlu_result.intent}, entities={nlu_result.entities}, language={nlu_result.language}")
response2 = conversation.handle_message(input2, session_id="test")
print(f"Response: {response2}")
if conversation.state:
    print(f"State slots: {conversation.state.slots}")
    missing = conversation.state.missing_slots()
    print(f"Missing: {missing if missing else 'NONE - READY TO EXECUTE! ✅'}")

# Round 3 - Try different natural language phrasing
print("\n🔵 ROUND 3: Another user providing info naturally (new session)")
print("-"*70)
conversation.state = None  # Reset
input3 = "I want pizza"
print(f"User: {input3}")
nlu_result = nlu.parse(input3)
print(f"NLU: intent={nlu_result.intent}, entities={nlu_result.entities}")
response3 = conversation.handle_message(input3, session_id="test3")
print(f"Response: {response3}")
print(f"Missing: {conversation.state.missing_slots()}")

print("\n🔵 ROUND 4: User says in full sentence")
print("-"*70)
input4 = "I want delivery, give me 3 items"
print(f"User: {input4}")
nlu_result = nlu.parse(input4)
print(f"NLU: intent={nlu_result.intent}, entities={nlu_result.entities}")
response4 = conversation.handle_message(input4, session_id="test3")
print(f"Response: {response4}")
if conversation.state:
    print(f"State slots: {conversation.state.slots}")
    missing = conversation.state.missing_slots()
    print(f"Missing: {missing if missing else 'NONE - READY! ✅'}")

# Round 5 - Try Sinhala
print("\n🔵 ROUND 5: User responds in Sinhala")
print("-"*70)
conversation.state = None
input5 = "පීසා එකක් order කරන්න"
print(f"User: {input5}")
nlu_result = nlu.parse(input5)
print(f"NLU: intent={nlu_result.intent}, entities={nlu_result.entities}, language={nlu_result.language}")
response5 = conversation.handle_message(input5, session_id="test4")
print(f"Response: {response5}")
print(f"Missing: {conversation.state.missing_slots()}")

print("\n🔵 ROUND 6: Sinhala user provides missing info")
print("-"*70)
input6 = "delivery එකක්, 2 ක්"
print(f"User: {input6}")
nlu_result = nlu.parse(input6)
print(f"NLU: intent={nlu_result.intent}, entities={nlu_result.entities}, language={nlu_result.language}")
response6 = conversation.handle_message(input6, session_id="test4")
print(f"Response: {response6}")
if conversation.state:
    print(f"State slots: {conversation.state.slots}")
    missing = conversation.state.missing_slots()
    print(f"Missing: {missing if missing else 'NONE - READY! ✅'}")

print("\n" + "="*70)
print("✅ TEST COMPLETE")
print("="*70)
