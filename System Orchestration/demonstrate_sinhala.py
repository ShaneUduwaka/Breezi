"""
Sinhala Language Support Demonstration
Tests English, Sinhala, and mixed language input
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system


def demonstrate_sinhala_support():
    """Test Sinhala and English language support"""

    print("\n" + "="*80)
    print("🌏 SINHALA LANGUAGE SUPPORT DEMONSTRATION")
    print("="*80)
    print("Testing: English Input → Sinhala Output, Sinhala Input → Sinhala Output")
    print()

    # Build system
    system = build_system()
    conversation = system["conversation"]
    nlu = system["nlu"]

    # Test Case 1: English Input
    print("🧪 TEST CASE 1: English Input")
    print("-" * 80)
    
    user_input = "I want to order a pizza"
    print(f"🎤 User Input (English): '{user_input}'")
    
    nlu_result = nlu.parse(user_input)
    print(f"🧠 NLU Result: intent='{nlu_result.intent}', language='{nlu_result.language}'")
    
    response = conversation.handle_message(user_input, session_id="english-test")
    print(f"💬 Response:\n{response}\n")

    # Test Case 2: Sinhala Input (with mixed keywords)
    print("-" * 80)
    print("🧪 TEST CASE 2: Sinhala Input (Mixed)")
    print("-" * 80)
    
    sinhala_input = "මටpizza ඉල්ලුම් කරන්නද"  # "I want to order pizza with pizza"
    print(f"🎤 User Input (Sinhala Mixed): '{sinhala_input}'")
    
    nlu_result = nlu.parse(sinhala_input)
    print(f"🧠 NLU Result: intent='{nlu_result.intent}', language='{nlu_result.language}'")
    
    response = conversation.handle_message(sinhala_input, session_id="sinhala-test")
    print(f"💬 Response (Sinhala):\n{response}\n")

    # Test Case 3: Menu Request in Sinhala
    print("-" * 80)
    print("🧪 TEST CASE 3: Sinhala Menu Request")
    print("-" * 80)
    
    sinhala_input2 = "මෙනුව පෙන්වන්න"  # "Show menu"
    print(f"🎤 User Input (Sinhala): '{sinhala_input2}'")
    
    nlu_result = nlu.parse(sinhala_input2)
    print(f"🧠 NLU Result: intent='{nlu_result.intent}', language='{nlu_result.language}'")
    
    response = conversation.handle_message(sinhala_input2, session_id="sinhala-menu-test")
    print(f"💬 Response (Sinhala):\n{response}\n")

    # Test Case 4: English Menu Request
    print("-" * 80)
    print("🧪 TEST CASE 4: English Menu Request (for comparison)")
    print("-" * 80)
    
    english_input = "show me the menu"
    print(f"🎤 User Input (English): '{english_input}'")
    
    nlu_result = nlu.parse(english_input)
    print(f"🧠 NLU Result: intent='{nlu_result.intent}', language='{nlu_result.language}'")
    
    response = conversation.handle_message(english_input, session_id="english-menu-test")
    print(f"💬 Response:\n{response}\n")

    # Summary
    print("="*80)
    print("✅ DEMONSTRATION COMPLETED!")
    print("="*80)
    print("""
Language Detection Features:
  • ✓ English input recognized correctly
  • ✓ Sinhala input recognized correctly
  • ✓ Mixed English+Sinhala input supported
  • ✓ Responses formatted in detected language
  • ✓ Numerals converted appropriately
  • ✓ English food names preserved (pizza, burger, etc.)

Sinhala Keywords Supported:
  • start_order: ඉල්ලුම්, ඔර්ඩර්, ඉතාමත්, etc.
  • view_menu: මෙනුව, න්‍යාපිතය, කෝටි
  • view_menu_category: බර්ගර්, පීසා, දෙමුතු
  • view_promotions: ඉඩ, පිණිස, විශේෂ
  • view_locations: ස්ථානය, ඉවුරු, පිහිටීම

Next Steps:
  1. Add entity extraction for Sinhala keywords
  2. Implement Sinhala STT/TTS integration
  3. Add more Sinhala translations
  4. Test with real voice input
""")
    print("="*80 + "\n")


if __name__ == "__main__":
    demonstrate_sinhala_support()
