
from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from .schema import SLOT_DEFINITIONS


LEXICON: Dict[str, List[str]] = {
    "food_item": [
        "චිකන් කොත්තු",
        "චීස් කොත්තු",
        "එග් ෆ්‍රයිඩ් රයිස්",
        "චිකන් ෆ්‍රයිඩ් රයිස්",
        "චිකන් බර්ගර්",
        "වෙජිටබල් නූඩ්ල්ස්",
        "චිකන් නූඩ්ල්ස්",
        "නාසි ගොරෙන්",
        "බිරියානි",
        "chicken kottu",
        "cheese kottu",
        "egg fried rice",
        "chicken fried rice",
        "chicken burger",
        "chicken burgers",
        "vegetable noodles",
        "chicken noodles",
        "nasi goreng",
        "biryani",
        "burger",
        "burgers",
        "fries",
        "drink",
        "kottu",
        "fried rice",
        "noodles",
    ],
    "category": [
        "kottu", "fried rice", "noodles", "desserts", "drinks", "seafood", "veg items"
    ],
    "order_type": [
        "delivery", "pickup", "takeaway", "dine in", "dine-in"
    ],
    "payment_method": [
        "cash", "card", "cash on delivery", "cod", "visa", "mastercard", "online payment",
        "cash වලින්", "කාඩ් එකෙන්",
    ],
    "portion_size": [
        "small", "medium", "large", "regular", "full", "half",
    ],
    "portion": [
        "small", "medium", "large", "regular", "full", "half",
    ],
    "item_variant": [
        "spicy", "mild", "cheese", "extra cheese", "veg", "vegetarian", "chicken", "egg",
    ],
    "diet": [
        "veg", "vegetarian", "vegan", "halal", "gluten free", "gluten-free",
    ],
    "promo_name": [
        "weekend combo", "family saver", "student deal", "buy one get one", "bogo"
    ],
    "offer_type": [
        "discount", "combo", "cashback", "offer", "deal"
    ],
    "urgency": [
        "now", "urgent", "asap", "immediately", "දැන්ම", "ඉක්මනට",
    ],
    "severity": [
        "low", "medium", "high", "urgent", "serious", "ගොඩක්",
    ],
    "allergen": [
        "nuts", "peanuts", "dairy", "milk", "gluten", "egg", "soy", "seafood",
    ],
    "ingredient": [
        "onion", "garlic", "soy sauce", "cheese", "egg", "nuts",
    ],
    "feedback_type": [
        "complaint", "suggestion", "feedback", "compliment",
    ],
    "membership_type": [
        "gold", "silver", "platinum", "student",
    ],
    "receipt_type": [
        "invoice", "receipt", "tax invoice"
    ],
    "field": [
        "phone number", "email", "address", "name",
    ],
    "branch": [
        "nugegoda", "maharagama", "kottawa", "battaramulla", "pannipitiya", "malabe",
        "නුගේගොඩ", "මහරගම", "කොට්ටාව", "බත්තරමුල්ල", "පන්නිපිටිය", "මාලබේ",
    ],
    "area": [
        "nugegoda", "maharagama", "kottawa", "battaramulla", "pannipitiya", "malabe",
    ],
    "day": [
        "today", "tomorrow", "monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday",
        "අද", "හෙට", "අනිද්දා", "සෙනසුරාදා", "ඉරිදා",
    ],
    "holiday": [
        "new year", "vesak", "christmas", "sinhala and tamil new year",
    ],
    "price_range": [
        "under 1000", "under 1500", "within 2000", "cheap", "budget", "premium",
    ],
    "topic": [
        "payment options", "promo rules", "membership", "delivery charges", "prices",
    ],
}


INTENT_EXAMPLES: Dict[str, List[str]] = {
    "start_new_order": [
        "I want to order",
        "place an order",
        "චිකන් කොත්තු එකක් දාන්න",
    ],
    "add_item_to_order": [
        "add this to my order",
        "add one more burger",
        "තවත් බර්ගර් එකක් දාන්න",
    ],
    "remove_item_from_order": [
        "remove the burger",
        "take off the noodles",
        "item එක අයින් කරන්න",
    ],
    "modify_item": [
        "change the burger to a chicken burger",
        "modify the kottu",
        "item එක මාරු කරන්න",
    ],
    "change_quantity": [
        "make it two",
        "change the quantity to 3",
        "quantity එක දෙකක් කරන්න",
    ],
    "view_current_cart": [
        "show my cart",
        "what's in my order",
        "cart එක පෙන්නන්න",
    ],
    "clear_cart": [
        "clear my cart",
        "remove all items",
        "cart එක empty කරන්න",
    ],
    "apply_coupon_promo": [
        "apply SAVE10",
        "use the family saver promo",
        "coupon code එක දාන්න",
    ],
    "ask_price_of_item": [
        "how much is the chicken kottu",
        "price of biryani",
        "මේකේ price එක කීයද",
    ],
    "ask_availability_of_item": [
        "is biryani available today",
        "do you have kottu now",
        "අද තියෙනවද",
    ],
    "customize_item": [
        "make it less spicy",
        "no onions please",
        "ලූනු නැතුව දෙන්න",
    ],
    "ask_for_recommendations": [
        "what do you recommend",
        "something spicy under 1500",
        "best veg option දෙන්න",
    ],
    "confirm_order": [
        "confirm my order",
        "place it",
        "order එක confirm කරන්න",
    ],
    "cancel_order_before_payment": [
        "cancel my order",
        "I don't want it anymore",
        "order එක cancel කරන්න",
    ],
    "reorder_previous_order": [
        "same as last time",
        "reorder my previous order",
    ],
    "choose_payment_method": [
        "I'll pay by card",
        "cash on delivery",
    ],
    "ask_accepted_payment_types": [
        "do you accept cards",
        "what payment methods are available",
    ],
    "payment_failed": [
        "my payment failed",
        "card payment didn't go through",
    ],
    "confirm_payment": [
        "I paid already",
        "payment completed",
    ],
    "refund_request": [
        "I need a refund",
        "refund my order",
    ],
    "split_payment": [
        "split the payment into two cards",
        "half cash half card",
    ],
    "ask_invoice_receipt": [
        "send me the invoice",
        "can I get a receipt",
    ],
    "choose_delivery": [
        "deliver it to Nugegoda",
        "I want delivery",
    ],
    "choose_pickup": [
        "I'll pick it up",
        "make it pickup",
    ],
    "change_delivery_address": [
        "change my address to Maharagama",
        "deliver to a different address",
    ],
    "add_delivery_instructions": [
        "call me when you arrive",
        "leave it at the gate",
    ],
    "ask_delivery_time_estimate": [
        "how long will delivery take",
        "when will it arrive",
    ],
    "track_order": [
        "track my order",
        "where is my order",
    ],
    "change_pickup_time": [
        "change pickup to 7 pm",
        "I’ll come later",
    ],
    "report_delivery_issue": [
        "the rider couldn't find the place",
        "delivery person called the wrong number",
    ],
    "report_missing_item": [
        "my drink is missing",
        "you forgot the fries",
    ],
    "late_delivery_complaint": [
        "my order is late",
        "it's been delayed a lot",
    ],
    "store_opening_hours": [
        "when do you open",
        "opening hours for Nugegoda",
    ],
    "store_location": [
        "where is your Maharagama branch",
        "store location",
    ],
    "holiday_schedule": [
        "are you open on New Year",
        "holiday hours",
    ],
    "parking_availability": [
        "is parking available",
        "do you have parking at night",
    ],
    "contact_details": [
        "give me the contact number",
        "branch contact details",
    ],
    "menu_inquiry": [
        "show me the menu",
        "what kottu do you have",
    ],
    "nutritional_information": [
        "calories in chicken burger",
        "nutrition for biryani",
    ],
    "allergen_information": [
        "does this contain nuts",
        "allergen info for kottu",
    ],
    "create_account": [
        "create an account for me",
        "sign me up",
    ],
    "login_help": [
        "I can't log in",
        "login problem",
    ],
    "reset_password": [
        "reset my password",
        "forgot password",
    ],
    "check_loyalty_points": [
        "check my points",
        "how many loyalty points do I have",
    ],
    "redeem_loyalty_points": [
        "redeem my points",
        "use points for this order",
    ],
    "ask_membership_benefits": [
        "what are the gold benefits",
        "membership benefits",
    ],
    "update_profile_info": [
        "change my phone number",
        "update my email",
    ],
    "file_complaint": [
        "I want to make a complaint",
        "this is unacceptable",
    ],
    "request_manager_callback": [
        "ask the manager to call me",
        "I want a callback",
    ],
    "report_bad_quality": [
        "the burger quality was bad",
        "food was stale",
    ],
    "refund_complaint": [
        "I want a refund because the food was wrong",
        "refund complaint",
    ],
    "escalation_request": [
        "escalate this issue",
        "I already reported this",
    ],
    "feedback_submission": [
        "I have feedback",
        "the service was great",
    ],
    "ask_ongoing_offers": [
        "what offers do you have",
        "any ongoing deals",
    ],
    "ask_specific_promo": [
        "tell me about the family saver promo",
        "how does student deal work",
    ],
    "subscribe_offers": [
        "subscribe me to offers",
        "send me promotions",
    ],
    "unsubscribe_marketing": [
        "stop sending me offers",
        "unsubscribe marketing messages",
    ],
    "bulk_catering_order": [
        "I need food for 50 people tomorrow",
        "bulk catering order",
    ],
    "event_booking": [
        "book an event for Friday evening",
        "reserve for 20 people",
    ],
}


SLOT_SYNONYMS: Dict[str, Dict[str, str]] = {
    "payment_method": {
        "cod": "cash on delivery",
        "cash": "cash",
        "cash on delivery": "cash on delivery",
        "card": "card",
        "visa": "card",
        "mastercard": "card",
        "කාඩ් එකෙන්": "card",
        "cash වලින්": "cash",
    },
    "order_type": {
        "delivery": "delivery",
        "pickup": "pickup",
        "takeaway": "pickup",
        "dine in": "dine_in",
        "dine-in": "dine_in",
    },
    "diet": {
        "veg": "vegetarian",
        "vegetarian": "vegetarian",
        "vegan": "vegan",
        "gluten free": "gluten_free",
        "gluten-free": "gluten_free",
    },
    "urgency": {
        "asap": "urgent",
        "urgent": "urgent",
        "immediately": "urgent",
        "දැන්ම": "urgent",
        "ඉක්මනට": "urgent",
    },
    "severity": {
        "serious": "high",
        "urgent": "high",
        "ගොඩක්": "high",
        "medium": "medium",
        "low": "low",
    },
}


def build_entity_ruler_patterns() -> List[dict]:
    patterns: List[dict] = []
    for label, values in LEXICON.items():
        for value in values:
            patterns.append({"label": label, "pattern": value})
    return patterns


def intent_corpus() -> List[Tuple[str, str]]:
    rows: List[Tuple[str, str]] = []
    for intent, texts in INTENT_EXAMPLES.items():
        rows.extend((intent, text) for text in texts)
    return rows
