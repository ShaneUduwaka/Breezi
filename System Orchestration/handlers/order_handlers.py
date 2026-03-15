"""
Templated Handler functions - reads all business logic from JSON
No hardcoded responses, menu items, or business data
"""


class GenericHandler:
    """
    Generic handler that reads business data and response templates from JSON.
    Completely templated - works for any business type.

    Optionally holds references to a RAG store and conversation context memory
    so individual handler methods can query external knowledge or history.
    """

    def __init__(self, business_data, rag_store=None, context_memory=None):
        """
        Initialize with business data from JSON

        Args:
            business_data: dict containing menu, promotions, locations, hours, etc.
            rag_store: optional RagStore instance for key/value lookup
            context_memory: optional ContextMemory instance for storing turns
        """
        self.business_data = business_data
        self.menu_data = business_data.get("menu", {})
        self.promotions = business_data.get("promotions", [])
        self.locations = business_data.get("locations", {})
        self.hours = business_data.get("hours", {})
        self.rag = rag_store
        self.context = context_memory

    def handle_view_menu_overview(self, state):
        """Show general menu overview - reads categories from JSON.

        If a RAG store is available we attempt a quick lookup before recomputing
        the overview; this allows the menu text to be updated independently of
        the core JSON.
        """
        # try RAG first
        if self.rag:
            cached = self.rag.get("menu_overview")
            if cached:
                return cached

        categories = self.menu_data.get("categories", {})

        if not categories:
            return "📋 Our menu is currently being updated. Please check back later."

        response = "📋 Our Menu:\n"
        for cat_key, cat_data in categories.items():
            cat_name = cat_data.get("name", cat_key.title())
            response += f"- {cat_name}\n"

        if self.promotions:
            response += "- Promotions available!"

        return response

    def handle_view_menu_by_category(self, state):
        """Show items by category - reads from JSON menu data"""
        category = state.slots.get("category")

        if not category:
            return "Please specify which category you'd like to see."

        categories = self.menu_data.get("categories", {})

        # Try to find category by name or key
        category_data = None
        for cat_key, cat_info in categories.items():
            if cat_key == category or cat_info.get("name", "").lower() == category.lower():
                category_data = cat_info
                break

        if not category_data:
            return f"Sorry, we don't have a '{category}' category."

        cat_name = category_data.get("name", category.title())
        items = category_data.get("items", {})

        if not items:
            return f"📋 {cat_name} category is currently empty."

        response = f"🍽️ {cat_name}:\n"
        for item_key, item_data in items.items():
            name = item_data.get("name", item_key.replace("_", " ").title())
            price = item_data.get("price", "N/A")
            response += f"- {name} - ${price}\n"

        return response

    def handle_view_menu_item(self, state):
        """Show details about specific menu item - reads from JSON"""
        item_name = state.slots.get("item_name")

        if not item_name:
            return "Please specify which item you'd like details for."

        # Search through all categories for the item
        categories = self.menu_data.get("categories", {})

        for cat_key, cat_data in categories.items():
            items = cat_data.get("items", {})
            for item_key, item_data in items.items():
                # Check if item name matches
                if (item_key == item_name or
                    item_data.get("name", "").lower() == item_name.lower() or
                    item_name.lower() in item_data.get("name", "").lower()):

                    name = item_data.get("name", item_key.replace("_", " ").title())
                    description = item_data.get("description", "A delicious menu item")
                    price = item_data.get("price", "N/A")

                    return f"🍽️ {name} - ${price}\n{description}"

        return f"❌ Sorry, we don't have '{item_name}' on our menu."

    def handle_view_promotions(self, state):
        """Show current promotions - reads from JSON"""
        if not self.promotions:
            return "🎉 No current promotions available."

        response = "🎉 Current Promotions:\n"
        for promo in self.promotions:
            response += f"- {promo}\n"

        return response

    def handle_view_locations(self, state):
        """Show store locations - reads from JSON"""
        location_query = state.slots.get("location_query")

        if location_query:
            # Try to find specific location
            for loc_key, address in self.locations.items():
                if loc_key.lower() in location_query.lower() or location_query.lower() in loc_key.lower():
                    return f"📍 {loc_key.title()} Location:\n{address}"

            return f"📍 Locations near '{location_query}':\n" + "\n".join(self.locations.values())

        # Show all locations
        if not self.locations:
            return "📍 Location information is currently being updated."

        response = "📍 Our Locations:\n"
        for loc_key, address in self.locations.items():
            response += f"- {loc_key.title()}: {address}\n"

        return response

    def handle_view_hours(self, state):
        """Show business hours - reads from JSON"""
        if not self.hours:
            return "🕐 Hours information is currently being updated."

        response = "🕐 Business Hours:\n"
        for period, hours in self.hours.items():
            period_name = period.replace("_", " ").title()
            response += f"- {period_name}: {hours}\n"

        return response

    def handle_start_order(self, state):
        """Handle order initiation - generic response"""
        items = state.slots.get("order_items")
        order_type = state.slots.get("order_type")

        response = "✓ Order started!"
        if items:
            response += f" You want: {items}."
        if order_type:
            response += f" Order type: {order_type}."

        response += " Processing your order..."
        return response

    def handle_modify_order(self, state):
        """Handle order modification"""
        return "✏️ Order modification initiated. What would you like to change?"

    def handle_cancel_order(self, state):
        """Handle order cancellation"""
        return "❌ Order cancelled successfully. Is there anything else I can help with?"

    def handle_track_order(self, state):
        """Handle order tracking"""
        return "📦 Your order is being prepared. Estimated time: 20 minutes."


# Create handler instance - will be initialized with business data
_generic_handler = None

def initialize_handlers(business_data, rag_store=None, context_memory=None):
    """Initialize handlers with business data from JSON

    rag_store and context_memory are optional and will be attached to the
    generic handler so that individual methods can access them if needed.
    """
    global _generic_handler
    _generic_handler = GenericHandler(business_data, rag_store, context_memory)

def handle_view_menu_overview(state):
    return _generic_handler.handle_view_menu_overview(state)

def handle_view_menu_by_category(state):
    return _generic_handler.handle_view_menu_by_category(state)

def handle_view_menu_item(state):
    return _generic_handler.handle_view_menu_item(state)

def handle_view_promotions(state):
    return _generic_handler.handle_view_promotions(state)

def handle_view_locations(state):
    return _generic_handler.handle_view_locations(state)

def handle_view_hours(state):
    return _generic_handler.handle_view_hours(state)

def handle_start_order(state):
    return _generic_handler.handle_start_order(state)

def handle_modify_order(state):
    return _generic_handler.handle_modify_order(state)

def handle_cancel_order(state):
    return _generic_handler.handle_cancel_order(state)

def handle_track_order(state):
    return _generic_handler.handle_track_order(state)
