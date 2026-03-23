
from pprint import pprint

from restaurant_nlu.dialogue import DialogueManager


def run_demo() -> None:
    bot = DialogueManager()

    examples = [
        "I want two chicken burgers delivered to Nugegoda with less spicy",
        "track my order ORD-5521",
        "apply SAVE10 to order 12345",
        "the food was bad and I need a refund for order A102",
        "book catering for 50 people tomorrow evening",
        "my name is Kasun and my phone number is 0712345678",
        "change pickup to 7 pm",
    ]

    for text in examples:
        print("=" * 100)
        print(f"INPUT: {text}")
        result = bot.handle(text)
        pprint(result)


if __name__ == "__main__":
    run_demo()
