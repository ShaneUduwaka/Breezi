
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Set


SlotKind = Literal["entity", "pattern", "free_text", "system"]
IntentKind = Literal["transaction", "question", "support", "contextual"]


@dataclass(frozen=True)
class SlotDefinition:
    name: str
    kind: SlotKind
    required: bool = True
    aliases: List[str] = field(default_factory=list)
    description: str = ""
    examples: List[str] = field(default_factory=list)
    regexes: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class IntentDefinition:
    name: str
    domain: str
    kind: IntentKind
    required_slots: List[str]
    optional_slots: List[str] = field(default_factory=list)
    priority_slots: List[str] = field(default_factory=list)
    contextual: bool = False
    description: str = ""


SLOT_DEFINITIONS: Dict[str, SlotDefinition] = {
    # menu and order core
    "food_item": SlotDefinition(
        name="food_item",
        kind="entity",
        aliases=["item", "dish"],
        description="Menu item requested by the user.",
        examples=["චිකන් කොත්තු", "chicken burger", "fried rice"],
    ),
    "quantity": SlotDefinition(
        name="quantity",
        kind="pattern",
        description="Number of units, portions, or packs.",
        examples=["1", "two", "දෙකක්"],
        regexes=[
            r"\b\d+\b",
        ],
    ),
    "order_type": SlotDefinition(
        name="order_type",
        kind="entity",
        required=False,
        examples=["delivery", "pickup", "takeaway", "dine-in"],
    ),
    "order_id": SlotDefinition(
        name="order_id",
        kind="pattern",
        description="Reference for an existing order.",
        examples=["12345", "A102", "ORD-2201"],
        regexes=[
            r"\b(?:ORD[-\s]?)?\d{4,8}\b",
            r"\b[A-Z]\d{3,6}\b",
        ],
    ),
    "modification_type": SlotDefinition(
        name="modification_type",
        kind="entity",
        examples=["remove onions", "extra cheese", "make it spicy"],
    ),
    "portion_size": SlotDefinition(
        name="portion_size",
        kind="entity",
        required=False,
        examples=["small", "medium", "large", "full", "half"],
    ),
    "item_variant": SlotDefinition(
        name="item_variant",
        kind="entity",
        required=False,
        examples=["spicy", "cheese", "veg", "chicken"],
    ),
    "special_request": SlotDefinition(
        name="special_request",
        kind="free_text",
        required=False,
        examples=["less spicy", "no onions", "extra gravy"],
    ),
    "food_preference": SlotDefinition(
        name="food_preference",
        kind="free_text",
        required=False,
        examples=["something spicy", "kid-friendly", "best seller"],
    ),
    "diet": SlotDefinition(
        name="diet",
        kind="entity",
        required=False,
        examples=["veg", "vegan", "halal", "gluten free"],
    ),
    "coupon_code": SlotDefinition(
        name="coupon_code",
        kind="pattern",
        required=False,
        examples=["SAVE10", "NEW50"],
        regexes=[r"\b[A-Z0-9]{4,12}\b"],
    ),
    "promo_name": SlotDefinition(
        name="promo_name",
        kind="entity",
        required=False,
        examples=["weekend combo", "family saver"],
    ),

    # payment
    "payment_method": SlotDefinition(
        name="payment_method",
        kind="entity",
        required=False,
        examples=["cash", "card", "cash on delivery", "visa"],
    ),
    "amount": SlotDefinition(
        name="amount",
        kind="pattern",
        required=False,
        examples=["1500", "Rs 2500", "LKR 1200"],
        regexes=[
            r"\b(?:Rs\.?|LKR)\s?\d+(?:[.,]\d{2})?\b",
            r"\b\d+(?:[.,]\d{2})?\s?(?:rs|lkr)\b",
            r"\b\d+(?:[.,]\d{2})?\b",
        ],
    ),
    "split": SlotDefinition(
        name="split",
        kind="free_text",
        required=False,
        examples=["split into two cards", "half cash half card"],
    ),
    "contact": SlotDefinition(
        name="contact",
        kind="free_text",
        required=False,
        examples=["send to my email", "WhatsApp me"],
    ),
    "receipt_type": SlotDefinition(
        name="receipt_type",
        kind="entity",
        required=False,
        aliases=["type"],
        examples=["invoice", "receipt", "tax invoice"],
    ),

    # delivery and pickup
    "delivery_address": SlotDefinition(
        name="delivery_address",
        kind="free_text",
        required=False,
        examples=["Nugegoda", "123 Main Street", "near the temple"],
    ),
    "landmark": SlotDefinition(
        name="landmark",
        kind="free_text",
        required=False,
        examples=["near the bank", "next to the school"],
    ),
    "instructions": SlotDefinition(
        name="instructions",
        kind="free_text",
        required=False,
        examples=["call when arriving", "leave at gate"],
    ),
    "pickup_time": SlotDefinition(
        name="pickup_time",
        kind="pattern",
        required=False,
        examples=["7 pm", "හතට", "tomorrow evening"],
        regexes=[
            r"\b\d{1,2}(?::\d{2})?\s?(?:am|pm|AM|PM)\b",
            r"\b\d{1,2}(?::\d{2})\b",
        ],
    ),
    "time": SlotDefinition(
        name="time",
        kind="pattern",
        required=False,
        examples=["7 pm", "evening"],
        regexes=[
            r"\b\d{1,2}(?::\d{2})?\s?(?:am|pm|AM|PM)\b",
            r"\b\d{1,2}(?::\d{2})\b",
        ],
    ),
    "delay": SlotDefinition(
        name="delay",
        kind="free_text",
        required=False,
        examples=["30 minutes", "one hour late"],
    ),
    "resolution": SlotDefinition(
        name="resolution",
        kind="free_text",
        required=False,
        examples=["refund", "replacement", "redelivery"],
    ),

    # store info
    "day": SlotDefinition(
        name="day",
        kind="entity",
        required=False,
        examples=["today", "tomorrow", "Monday", "අද"],
    ),
    "branch": SlotDefinition(
        name="branch",
        kind="entity",
        required=False,
        examples=["Nugegoda branch", "Maharagama"],
    ),
    "area": SlotDefinition(
        name="area",
        kind="entity",
        required=False,
        examples=["Nugegoda", "Colombo 05"],
    ),
    "holiday": SlotDefinition(
        name="holiday",
        kind="entity",
        required=False,
        examples=["New Year", "Vesak"],
    ),
    "availability": SlotDefinition(
        name="availability",
        kind="system",
        required=False,
        examples=["available", "not available"],
    ),
    "category": SlotDefinition(
        name="category",
        kind="entity",
        required=False,
        examples=["kottu", "fried rice", "noodles", "desserts"],
    ),
    "nutrition": SlotDefinition(
        name="nutrition",
        kind="system",
        required=False,
        examples=["calories", "protein"],
    ),
    "portion": SlotDefinition(
        name="portion",
        kind="entity",
        required=False,
        examples=["small", "large", "full"],
    ),
    "allergen": SlotDefinition(
        name="allergen",
        kind="entity",
        required=False,
        examples=["nuts", "dairy", "gluten"],
    ),
    "ingredient": SlotDefinition(
        name="ingredient",
        kind="entity",
        required=False,
        examples=["cheese", "soy sauce"],
    ),

    # account and identity
    "name": SlotDefinition(
        name="name",
        kind="free_text",
        required=False,
        examples=["Kamal", "Nimali"],
    ),
    "phone_number": SlotDefinition(
        name="phone_number",
        kind="pattern",
        required=False,
        examples=["0712345678", "+94 71 234 5678"],
        regexes=[
            r"(?:\+94|0)\s?7\d{1}\s?\d{3}\s?\d{4}",
        ],
    ),
    "email": SlotDefinition(
        name="email",
        kind="pattern",
        required=False,
        examples=["name@example.com"],
        regexes=[
            r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}\b",
        ],
    ),
    "issue": SlotDefinition(
        name="issue",
        kind="free_text",
        required=False,
        examples=["payment failed", "wrong item", "can't log in"],
    ),
    "account": SlotDefinition(
        name="account",
        kind="entity",
        required=False,
        examples=["my account", "loyalty account"],
    ),
    "id": SlotDefinition(
        name="id",
        kind="pattern",
        required=False,
        examples=["M1002", "USR-12345"],
        regexes=[
            r"\b[A-Z]{1,4}[- ]?\d{3,8}\b",
        ],
    ),
    "points": SlotDefinition(
        name="points",
        kind="pattern",
        required=False,
        examples=["100 points", "250"],
        regexes=[r"\b\d+\b"],
    ),
    "field": SlotDefinition(
        name="field",
        kind="entity",
        required=False,
        examples=["phone number", "email", "address"],
    ),
    "value": SlotDefinition(
        name="value",
        kind="free_text",
        required=False,
        examples=["new phone number", "new email address"],
    ),

    # support and complaints
    "severity": SlotDefinition(
        name="severity",
        kind="entity",
        required=False,
        examples=["low", "medium", "high", "urgent"],
    ),
    "previous": SlotDefinition(
        name="previous",
        kind="free_text",
        required=False,
        examples=["I already called", "I reported this yesterday"],
    ),
    "message": SlotDefinition(
        name="message",
        kind="free_text",
        required=False,
        examples=["The food was good but delivery was slow"],
    ),
    "feedback_type": SlotDefinition(
        name="feedback_type",
        kind="entity",
        required=False,
        aliases=["type"],
        examples=["compliment", "complaint", "suggestion"],
    ),
    "reason": SlotDefinition(
        name="reason",
        kind="free_text",
        required=False,
        examples=["ordered by mistake", "too late", "changed my mind"],
    ),
    "urgency": SlotDefinition(
        name="urgency",
        kind="entity",
        required=False,
        examples=["now", "urgent", "as soon as possible"],
    ),

    # offers and marketing
    "offer_type": SlotDefinition(
        name="offer_type",
        kind="entity",
        required=False,
        examples=["discount", "combo", "cashback"],
    ),
    "topic": SlotDefinition(
        name="topic",
        kind="entity",
        required=False,
        examples=["payment options", "promo rules"],
    ),
    "membership_type": SlotDefinition(
        name="membership_type",
        kind="entity",
        required=False,
        aliases=["type"],
        examples=["gold", "silver", "student"],
    ),
    "benefit": SlotDefinition(
        name="benefit",
        kind="system",
        required=False,
        examples=["free delivery", "extra points"],
    ),

    # catering and events
    "event_date": SlotDefinition(
        name="event_date",
        kind="pattern",
        required=False,
        examples=["tomorrow", "2026-04-02", "next Friday"],
        regexes=[
            r"\b\d{4}-\d{2}-\d{2}\b",
            r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        ],
    ),
    "event_time": SlotDefinition(
        name="event_time",
        kind="pattern",
        required=False,
        examples=["6 pm", "18:30"],
        regexes=[
            r"\b\d{1,2}(?::\d{2})?\s?(?:am|pm|AM|PM)\b",
            r"\b\d{1,2}:\d{2}\b",
        ],
    ),
    "headcount": SlotDefinition(
        name="headcount",
        kind="pattern",
        required=False,
        examples=["50 people", "10 pax", "8"],
        regexes=[
            r"\b\d+\s?(?:people|persons|pax|guests)?\b",
        ],
    ),
    "status": SlotDefinition(
        name="status",
        kind="system",
        required=False,
        examples=["confirmed", "pending", "paid"],
    ),
    "date": SlotDefinition(
        name="date",
        kind="pattern",
        required=False,
        examples=["today", "tomorrow", "2026-03-25"],
        regexes=[
            r"\b\d{4}-\d{2}-\d{2}\b",
            r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
        ],
    ),
    "previous_order": SlotDefinition(
        name="previous_order",
        kind="free_text",
        required=False,
        examples=["same as last time", "my last order"],
    ),
}

INTENT_DEFINITIONS: Dict[str, IntentDefinition] = {
    # ordering
    "start_new_order": IntentDefinition(
        name="start_new_order",
        domain="ordering",
        kind="transaction",
        required_slots=["food_item"],
        optional_slots=["quantity", "order_type", "special_request", "item_variant"],
        priority_slots=["food_item", "quantity"],
        description="Begin a fresh order.",
    ),
    "add_item_to_order": IntentDefinition(
        name="add_item_to_order",
        domain="ordering",
        kind="contextual",
        required_slots=["food_item"],
        optional_slots=["order_id", "quantity"],
        priority_slots=["food_item", "quantity"],
        contextual=True,
    ),
    "remove_item_from_order": IntentDefinition(
        name="remove_item_from_order",
        domain="ordering",
        kind="contextual",
        required_slots=["food_item"],
        optional_slots=["order_id", "quantity"],
        priority_slots=["food_item"],
        contextual=True,
    ),
    "modify_item": IntentDefinition(
        name="modify_item",
        domain="ordering",
        kind="contextual",
        required_slots=["food_item", "modification_type"],
        optional_slots=["order_id"],
        priority_slots=["food_item", "modification_type"],
        contextual=True,
    ),
    "change_quantity": IntentDefinition(
        name="change_quantity",
        domain="ordering",
        kind="contextual",
        required_slots=["food_item", "quantity"],
        optional_slots=["order_id"],
        priority_slots=["food_item", "quantity"],
        contextual=True,
    ),
    "view_current_cart": IntentDefinition(
        name="view_current_cart",
        domain="ordering",
        kind="question",
        required_slots=[],
        optional_slots=["order_id", "name", "phone_number"],
    ),
    "clear_cart": IntentDefinition(
        name="clear_cart",
        domain="ordering",
        kind="transaction",
        required_slots=[],
        optional_slots=["order_id", "name"],
        priority_slots=["order_id"],
        description="Clear all items from cart.",
    ),
    "apply_coupon_promo": IntentDefinition(
        name="apply_coupon_promo",
        domain="payment",
        kind="transaction",
        required_slots=[],
        optional_slots=["order_id", "coupon_code", "promo_name"],
        priority_slots=["coupon_code", "promo_name", "order_id"],
    ),
    "ask_price_of_item": IntentDefinition(
        name="ask_price_of_item",
        domain="menu",
        kind="question",
        required_slots=["food_item"],
        optional_slots=["portion_size", "item_variant"],
        priority_slots=["food_item"],
    ),
    "ask_availability_of_item": IntentDefinition(
        name="ask_availability_of_item",
        domain="menu",
        kind="question",
        required_slots=["food_item"],
        optional_slots=["date", "item_variant"],
        priority_slots=["food_item"],
    ),
    "customize_item": IntentDefinition(
        name="customize_item",
        domain="ordering",
        kind="contextual",
        required_slots=["food_item", "special_request"],
        optional_slots=["quantity"],
        priority_slots=["food_item", "special_request"],
        contextual=True,
    ),
    "ask_for_recommendations": IntentDefinition(
        name="ask_for_recommendations",
        domain="menu",
        kind="question",
        required_slots=[],
        optional_slots=["food_preference", "price_range", "diet"],
        priority_slots=["food_preference", "diet"],
    ),
    "confirm_order": IntentDefinition(
        name="confirm_order",
        domain="ordering",
        kind="transaction",
        required_slots=[],
        optional_slots=["order_id", "name"],
        priority_slots=["order_id"],
    ),
    "cancel_order_before_payment": IntentDefinition(
        name="cancel_order_before_payment",
        domain="ordering",
        kind="transaction",
        required_slots=[],
        optional_slots=["order_id", "reason", "urgency"],
        priority_slots=["order_id"],
    ),
    "reorder_previous_order": IntentDefinition(
        name="reorder_previous_order",
        domain="ordering",
        kind="transaction",
        required_slots=[],
        optional_slots=["previous_order", "name", "phone_number"],
        priority_slots=["previous_order", "phone_number"],
    ),

    # payment
    "choose_payment_method": IntentDefinition(
        name="choose_payment_method",
        domain="payment",
        kind="transaction",
        required_slots=["payment_method"],
        optional_slots=["order_id", "amount"],
        priority_slots=["payment_method"],
    ),
    "ask_accepted_payment_types": IntentDefinition(
        name="ask_accepted_payment_types",
        domain="payment",
        kind="question",
        required_slots=[],
        optional_slots=["topic", "branch", "payment_method"],
    ),
    "payment_failed": IntentDefinition(
        name="payment_failed",
        domain="payment",
        kind="support",
        required_slots=[],
        optional_slots=["order_id", "payment_method", "issue"],
        priority_slots=["issue", "order_id"],
    ),
    "confirm_payment": IntentDefinition(
        name="confirm_payment",
        domain="payment",
        kind="transaction",
        required_slots=[],
        optional_slots=["order_id", "payment_method", "amount"],
        priority_slots=["order_id", "payment_method"],
    ),
    "refund_request": IntentDefinition(
        name="refund_request",
        domain="payment",
        kind="support",
        required_slots=[],
        optional_slots=["order_id", "reason", "amount"],
        priority_slots=["order_id", "reason"],
    ),
    "split_payment": IntentDefinition(
        name="split_payment",
        domain="payment",
        kind="transaction",
        required_slots=[],
        optional_slots=["order_id", "split", "amount"],
        priority_slots=["split", "amount"],
    ),
    "ask_invoice_receipt": IntentDefinition(
        name="ask_invoice_receipt",
        domain="payment",
        kind="question",
        required_slots=[],
        optional_slots=["order_id", "receipt_type", "contact"],
        priority_slots=["order_id", "receipt_type"],
    ),

    # fulfillment
    "choose_delivery": IntentDefinition(
        name="choose_delivery",
        domain="fulfillment",
        kind="transaction",
        required_slots=["delivery_address"],
        optional_slots=["food_item", "quantity", "landmark", "instructions"],
        priority_slots=["delivery_address"],
        description="Switch or set the order to delivery.",
    ),
    "choose_pickup": IntentDefinition(
        name="choose_pickup",
        domain="fulfillment",
        kind="transaction",
        required_slots=[],
        optional_slots=["food_item", "quantity", "pickup_time"],
        priority_slots=["pickup_time"],
    ),
    "change_delivery_address": IntentDefinition(
        name="change_delivery_address",
        domain="fulfillment",
        kind="transaction",
        required_slots=["delivery_address"],
        optional_slots=["order_id", "landmark"],
        priority_slots=["delivery_address"],
    ),
    "add_delivery_instructions": IntentDefinition(
        name="add_delivery_instructions",
        domain="fulfillment",
        kind="contextual",
        required_slots=["instructions"],
        optional_slots=["order_id", "landmark"],
        priority_slots=["instructions"],
        contextual=True,
    ),
    "ask_delivery_time_estimate": IntentDefinition(
        name="ask_delivery_time_estimate",
        domain="fulfillment",
        kind="question",
        required_slots=[],
        optional_slots=["order_id", "delivery_address", "time"],
        priority_slots=["order_id", "delivery_address"],
    ),
    "track_order": IntentDefinition(
        name="track_order",
        domain="fulfillment",
        kind="question",
        required_slots=[],
        optional_slots=["order_id", "phone_number", "name"],
        priority_slots=["order_id", "phone_number"],
    ),
    "change_pickup_time": IntentDefinition(
        name="change_pickup_time",
        domain="fulfillment",
        kind="transaction",
        required_slots=["pickup_time"],
        optional_slots=["order_id", "name"],
        priority_slots=["pickup_time"],
    ),
    "report_delivery_issue": IntentDefinition(
        name="report_delivery_issue",
        domain="support",
        kind="support",
        required_slots=["issue"],
        optional_slots=["order_id", "resolution"],
        priority_slots=["issue", "order_id"],
    ),
    "report_missing_item": IntentDefinition(
        name="report_missing_item",
        domain="support",
        kind="support",
        required_slots=["food_item"],
        optional_slots=["order_id", "resolution"],
        priority_slots=["food_item", "order_id"],
    ),
    "late_delivery_complaint": IntentDefinition(
        name="late_delivery_complaint",
        domain="support",
        kind="support",
        required_slots=["issue"],
        optional_slots=["order_id", "delay"],
        priority_slots=["issue", "order_id"],
    ),

    # store info
    "store_opening_hours": IntentDefinition(
        name="store_opening_hours",
        domain="store_info",
        kind="question",
        required_slots=[],
        optional_slots=["day", "time", "branch"],
        priority_slots=["branch", "day"],
    ),
    "store_location": IntentDefinition(
        name="store_location",
        domain="store_info",
        kind="question",
        required_slots=[],
        optional_slots=["branch", "area", "landmark"],
        priority_slots=["branch", "area"],
    ),
    "holiday_schedule": IntentDefinition(
        name="holiday_schedule",
        domain="store_info",
        kind="question",
        required_slots=[],
        optional_slots=["day", "holiday", "branch"],
        priority_slots=["holiday", "branch"],
    ),
    "parking_availability": IntentDefinition(
        name="parking_availability",
        domain="store_info",
        kind="question",
        required_slots=[],
        optional_slots=["branch", "time"],
        priority_slots=["branch"],
    ),
    "contact_details": IntentDefinition(
        name="contact_details",
        domain="store_info",
        kind="question",
        required_slots=[],
        optional_slots=["branch", "receipt_type", "time"],
        priority_slots=["branch"],
    ),
    "menu_inquiry": IntentDefinition(
        name="menu_inquiry",
        domain="menu",
        kind="question",
        required_slots=[],
        optional_slots=["category", "food_item", "price_range"],
        priority_slots=["category", "food_item"],
    ),
    "nutritional_information": IntentDefinition(
        name="nutritional_information",
        domain="menu",
        kind="question",
        required_slots=["food_item"],
        optional_slots=["portion"],
        priority_slots=["food_item"],
    ),
    "allergen_information": IntentDefinition(
        name="allergen_information",
        domain="menu",
        kind="question",
        required_slots=["food_item"],
        optional_slots=["allergen", "ingredient"],
        priority_slots=["food_item"],
    ),

    # account
    "create_account": IntentDefinition(
        name="create_account",
        domain="account",
        kind="transaction",
        required_slots=["name"],
        optional_slots=["phone_number", "email"],
        priority_slots=["name", "phone_number"],
    ),
    "login_help": IntentDefinition(
        name="login_help",
        domain="account",
        kind="support",
        required_slots=[],
        optional_slots=["phone_number", "email", "issue"],
        priority_slots=["phone_number", "email", "issue"],
    ),
    "reset_password": IntentDefinition(
        name="reset_password",
        domain="account",
        kind="transaction",
        required_slots=[],
        optional_slots=["phone_number", "email", "account"],
        priority_slots=["phone_number", "email"],
    ),
    "check_loyalty_points": IntentDefinition(
        name="check_loyalty_points",
        domain="account",
        kind="question",
        required_slots=[],
        optional_slots=["phone_number", "name", "id"],
        priority_slots=["id", "phone_number"],
    ),
    "redeem_loyalty_points": IntentDefinition(
        name="redeem_loyalty_points",
        domain="account",
        kind="transaction",
        required_slots=[],
        optional_slots=["id", "points", "order_id"],
        priority_slots=["points", "order_id"],
    ),
    "ask_membership_benefits": IntentDefinition(
        name="ask_membership_benefits",
        domain="account",
        kind="question",
        required_slots=[],
        optional_slots=["membership_type", "topic"],
        priority_slots=["membership_type"],
    ),
    "update_profile_info": IntentDefinition(
        name="update_profile_info",
        domain="account",
        kind="transaction",
        required_slots=["field", "value"],
        optional_slots=["account"],
        priority_slots=["field", "value"],
    ),

    # support
    "file_complaint": IntentDefinition(
        name="file_complaint",
        domain="support",
        kind="support",
        required_slots=["issue"],
        optional_slots=["order_id", "severity"],
        priority_slots=["issue", "order_id"],
    ),
    "request_manager_callback": IntentDefinition(
        name="request_manager_callback",
        domain="support",
        kind="support",
        required_slots=["name"],
        optional_slots=["phone_number", "time"],
        priority_slots=["name", "phone_number"],
    ),
    "report_bad_quality": IntentDefinition(
        name="report_bad_quality",
        domain="support",
        kind="support",
        required_slots=["food_item", "issue"],
        optional_slots=["order_id"],
        priority_slots=["food_item", "issue"],
    ),
    "refund_complaint": IntentDefinition(
        name="refund_complaint",
        domain="support",
        kind="support",
        required_slots=["issue"],
        optional_slots=["order_id", "amount"],
        priority_slots=["issue", "order_id"],
    ),
    "escalation_request": IntentDefinition(
        name="escalation_request",
        domain="support",
        kind="support",
        required_slots=["issue"],
        optional_slots=["order_id", "previous"],
        priority_slots=["issue", "order_id"],
    ),
    "feedback_submission": IntentDefinition(
        name="feedback_submission",
        domain="support",
        kind="support",
        required_slots=["message"],
        optional_slots=["order_id", "feedback_type"],
        priority_slots=["message"],
    ),

    # marketing
    "ask_ongoing_offers": IntentDefinition(
        name="ask_ongoing_offers",
        domain="marketing",
        kind="question",
        required_slots=[],
        optional_slots=["offer_type", "day", "category"],
        priority_slots=["offer_type", "category"],
    ),
    "ask_specific_promo": IntentDefinition(
        name="ask_specific_promo",
        domain="marketing",
        kind="question",
        required_slots=["promo_name"],
        optional_slots=["topic", "food_item"],
        priority_slots=["promo_name"],
    ),
    "subscribe_offers": IntentDefinition(
        name="subscribe_offers",
        domain="marketing",
        kind="transaction",
        required_slots=[],
        optional_slots=["phone_number", "name", "contact"],
        priority_slots=["phone_number", "email"],
    ),
    "unsubscribe_marketing": IntentDefinition(
        name="unsubscribe_marketing",
        domain="marketing",
        kind="transaction",
        required_slots=[],
        optional_slots=["phone_number", "email", "contact"],
        priority_slots=["phone_number", "email"],
    ),

    # catering
    "bulk_catering_order": IntentDefinition(
        name="bulk_catering_order",
        domain="events",
        kind="transaction",
        required_slots=["event_date", "headcount"],
        optional_slots=["food_preference"],
        priority_slots=["event_date", "headcount"],
    ),
    "event_booking": IntentDefinition(
        name="event_booking",
        domain="events",
        kind="transaction",
        required_slots=["event_date", "event_time", "headcount"],
        optional_slots=[],
        priority_slots=["event_date", "event_time", "headcount"],
    ),
}


INTENT_GROUPS: Dict[str, Set[str]] = {
    "ordering": {
        "start_new_order", "add_item_to_order", "remove_item_from_order",
        "modify_item", "change_quantity", "view_current_cart", "clear_cart",
        "customize_item", "confirm_order", "cancel_order_before_payment",
        "reorder_previous_order",
    },
    "payment": {
        "apply_coupon_promo", "choose_payment_method", "ask_accepted_payment_types",
        "payment_failed", "confirm_payment", "refund_request", "split_payment",
        "ask_invoice_receipt",
    },
    "fulfillment": {
        "choose_delivery", "choose_pickup", "change_delivery_address",
        "add_delivery_instructions", "ask_delivery_time_estimate", "track_order",
        "change_pickup_time",
    },
    "support": {
        "report_delivery_issue", "report_missing_item", "late_delivery_complaint",
        "file_complaint", "request_manager_callback", "report_bad_quality",
        "refund_complaint", "escalation_request", "feedback_submission",
    },
    "store_info": {
        "store_opening_hours", "store_location", "holiday_schedule",
        "parking_availability", "contact_details",
    },
    "menu": {
        "ask_price_of_item", "ask_availability_of_item", "menu_inquiry",
        "nutritional_information", "allergen_information", "ask_for_recommendations",
    },
    "account": {
        "create_account", "login_help", "reset_password", "check_loyalty_points",
        "redeem_loyalty_points", "ask_membership_benefits", "update_profile_info",
    },
    "marketing": {
        "ask_ongoing_offers", "ask_specific_promo", "subscribe_offers",
        "unsubscribe_marketing",
    },
    "events": {
        "bulk_catering_order", "event_booking",
    },
}

OPTIONAL_DEFAULTS: Dict[str, List[str]] = {
    "choose_delivery": ["landmark", "instructions"],
    "start_new_order": ["quantity", "order_type", "special_request"],
    "customize_item": ["quantity"],
    "add_delivery_instructions": ["landmark"],
    "ask_for_recommendations": ["price_range", "diet"],
    "track_order": ["name"],
    "create_account": ["email"],
}


def get_required_slots(intent: str) -> List[str]:
    return list(INTENT_DEFINITIONS[intent].required_slots)


def get_optional_slots(intent: str) -> List[str]:
    return list(INTENT_DEFINITIONS[intent].optional_slots)


def get_priority_slots(intent: str) -> List[str]:
    definition = INTENT_DEFINITIONS[intent]
    return list(definition.priority_slots or definition.required_slots)


def get_all_slots_for_intent(intent: str) -> List[str]:
    definition = INTENT_DEFINITIONS[intent]
    seen: List[str] = []
    for slot in definition.required_slots + definition.optional_slots:
        if slot not in seen:
            seen.append(slot)
    return seen
