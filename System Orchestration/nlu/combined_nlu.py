import json
import sys
import os
from pathlib import Path

from Tier1.tier1_nlu import Tier1NLU
from Tier2.tier2_semantic import Tier2SemanticRouter


class CombinedNLU:
    def __init__(self):
        self.tier1 = Tier1NLU(model_path="Tier1/tier1_model.pkl")
        self.tier2 = None

        # Load Tier 1 model
        try:
            self.tier1.load_model()
            print("✓ Tier 1 model loaded successfully")
        except FileNotFoundError:
            print("✗ Tier 1 model not found. Please run Tier1/tier1_nlu.py first")
            return

        # Load Tier 2 index
        try:
            self.tier2 = Tier2SemanticRouter(
                index_path="Tier2/tier2_index.pkl",
                confidence_threshold=0.78,
                top_k=5,
            )
            print("✓ Tier 2 index loaded successfully")
        except FileNotFoundError:
            print("✗ Tier 2 index not found. Please run Tier2/build_tier2_index.py first")
            print("  Continuing with Tier 1 only...")

    def predict(self, user_text: str) -> dict:
        """Run both tiers and return the best prediction"""

        # Always run Tier 1 first
        print(f"  → Trying Tier 1...")
        tier1_result = self.tier1.predict(user_text)
        print(f"    Tier 1 result: {tier1_result['intent']} ({tier1_result['confidence']:.4f}) - {tier1_result['status']}")

        # If Tier 1 is successful, return it
        if tier1_result["status"] == "SUCCESS":
            return {
                "final_result": tier1_result,
                "tier_used": 1,
                "confidence": tier1_result["confidence"],
                "intent": tier1_result["intent"],
                "source": tier1_result["source"]
            }

        # If Tier 1 failed and we have Tier 2, try it
        if self.tier2:
            print(f"  → Tier 1 failed, trying Tier 2...")
            tier2_result = self.tier2.predict(user_text)
            print(f"    Tier 2 result: {tier2_result['intent']} ({tier2_result['confidence']:.4f}) - {tier2_result['status']}")

            if tier2_result["status"] == "SUCCESS":
                return {
                    "final_result": tier2_result,
                    "tier_used": 2,
                    "confidence": tier2_result["confidence"],
                    "intent": tier2_result["intent"],
                    "source": tier2_result["source"]
                }

    def run_tests(self):
        """Run predefined test cases with Sinhala inputs"""
        test_cases = [
            "මම මෙතනින් නිතරම කෑම ඕඩර් කරන කෙනෙක්, මගේ නම්බර් එක සේව් කරගෙන ලියාපදිංචි වෙන්න පුළුවන්ද?",
            "මට බත් 2ක් අද හවස 6ට ගන්න පුළුවන්ද?",
            "ඔයාලගෙ කෑම මොනවද තියෙන්නේ?",
            "මගේ කෑම එක කොහෙද තියෙන්නේ?",
            "හෙලෝ, මම සුදත්. මගේ order එක ටිකක් පරක්කු වගේ, order number එක 4521, මේකෙ ස්ටේටස් එක පොඩ්ඩක් බලල කියන්න පුලුවන්ද 0771234567 නම්බර් එකට දැම්මේ",
            "හෙලෝ, මම අද දවල් ඔයාලගෙන් කෑම ඕඩර් එකක් ගත්තා. ඒකේ physical receipt එකක් මට ඕනේ, ඒක ගන්න මොකක්ද කරන්නේ?"
        ]

        print("\n" + "="*80)
        print("RUNNING NLU TESTS - Sinhala Inputs")
        print("="*80)

        for i, test_input in enumerate(test_cases, 1):
            print(f"\nTest {i}: {test_input}")
            print("-" * 60)

            result = self.predict(test_input)

            print(f"Tier Used: {result['tier_used']}")
            print(f"Intent: {result['intent']}")
            print(f"Confidence: {result['confidence']:.4f}")
            print(f"Source: {result['source']}")
            print(f"Status: {result.get('status', result['final_result']['status'])}")

        print("\n" + "="*80)
        print("TESTS COMPLETED")
        print("="*80)


def main():
    print("=" * 60)
    print("Combined NLU System - Tier 1 + Tier 2")
    print("=" * 60)

    # Check for test flag
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Initialize combined NLU
        nlu = CombinedNLU()
        nlu.run_tests()
        return

    # Initialize combined NLU
    nlu = CombinedNLU()

    if len(sys.argv) > 1:
        # Command line mode
        user_input = " ".join(sys.argv[1:])
        print(f"\nInput: {user_input}")
        print("-" * 40)

        result = nlu.predict(user_input)

        print(f"Tier Used: {result['tier_used']}")
        print(f"Intent: {result['intent']}")
        print(f"Confidence: {result['confidence']:.4f}")
        print(f"Source: {result['source']}")
        print(f"Status: {result.get('status', result['final_result']['status'])}")

        if 'reason' in result:
            print(f"Reason: {result['reason']}")

        print("\nFull Result:")
        print(json.dumps(result['final_result'], indent=2, default=str))

    else:
        # Interactive mode
        print("\nInteractive Mode - Enter sentences to test NLU")
        print("Type 'quit' to exit")
        print("-" * 40)

        while True:
            try:
                user_input = input("\nEnter text: ").strip()
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break
                if not user_input:
                    continue

                result = nlu.predict(user_input)

                print(f"→ Tier {result['tier_used']}: {result['intent']} "
                      f"(confidence: {result['confidence']:.4f})")

                if result.get('status') == 'FALLBACK':
                    print(f"   ⚠️  {result.get('reason', 'Low confidence')}")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()