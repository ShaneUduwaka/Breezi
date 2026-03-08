"""
Handler mapping - Maps intent handler names to actual functions
"""

from handlers.order_handlers import (
    handle_start_order,
    handle_view_menu_overview,
    handle_view_menu_by_category,
    handle_view_menu_item,
    handle_view_promotions,
    handle_view_locations,
    handle_view_hours,
    handle_modify_order,
    handle_cancel_order,
    handle_track_order,
)

# Map handler names (from JSON) to actual functions
HANDLERS = {
    "handle_start_order": handle_start_order,
    "handle_view_menu_overview": handle_view_menu_overview,
    "handle_view_menu_by_category": handle_view_menu_by_category,
    "handle_view_menu_item": handle_view_menu_item,
    "handle_view_promotions": handle_view_promotions,
    "handle_view_locations": handle_view_locations,
    "handle_view_hours": handle_view_hours,
    "handle_modify_order": handle_modify_order,
    "handle_cancel_order": handle_cancel_order,
    "handle_track_order": handle_track_order,
}
