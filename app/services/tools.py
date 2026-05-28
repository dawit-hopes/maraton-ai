import json
from functools import lru_cache
from typing import Dict, Any

from app.core.config import settings


@lru_cache
def _load_food_data() -> dict:
    with open(settings.FOOD_DATA_PATH, "r") as f:
        return json.load(f)


def get_menu_item(item_name: str) -> dict:
    food_data = _load_food_data()
    query = item_name.lower().strip()

    for location in food_data.get("locations", {}).values():
        for outlet in location.get("outlets", []):
            for item in outlet.get("menu_items", []):
                name = item["name"].lower()
                if query in name or name in query:
                    return {
                        "found": True,
                        "location": location["display_name"],
                        "outlet": outlet["name"],
                        "item": item,
                    }

    for item in food_data.get("signature_dishes", []):
        name = item["name"].lower()
        if query in name or name in query:
            return {"found": True, "item": item, "note": "Available across Haile properties"}

    return {
        "found": False,
        "message": f"No menu item matching '{item_name}' was found. Ask about signature Ethiopian dishes or room service options.",
    }


def create_service_request(
    service_type: str,
    room_number: str,
    notes: str = None
) -> dict:
    # make the actual request to the service provider
    pass

    return {
        "success": True,
        "message": f"{service_type} request created for room {room_number}",
        "notes": notes
    }


def place_room_order(room_number: str, items: list) -> dict:
    #     make the actual request to the restaurant
    pass

    return {
        "success": True,
        "message": f"Room {room_number} order placed for {items}",
        "estimated_minutes": 20
    }



def execute_tool(name: str, args: dict) -> dict:
    if name == "create_service_request":
        return create_service_request(**args)
    elif name == "place_room_order":
        return place_room_order(**args)
    elif name == "get_menu_item":
        return get_menu_item(**args)

    return {"error": "Unknown tool"}



tools = [
    {
        "function_declarations": [
            {
                "name": "create_service_request",
                "description": "Creates a hotel service request when a guest asks for something like extra towels, pillows, room cleaning, wake-up call, laundry, or airport transfer.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service_type": {
                            "type": "string",
                            "description": "Type of service requested",
                            "enum": [
                                "extra_towels",
                                "extra_pillows",
                                "extra_blankets",
                                "room_cleaning",
                                "laundry_pickup",
                                "wake_up_call",
                                "airport_transfer",
                                "late_checkout",
                                "do_not_disturb"
                            ]
                        },
                        "room_number": {
                            "type": "string",
                            "description": "The room number making the request"
                        },
                        "notes": {
                            "type": "string",
                            "description": "Any extra details like wake-up time or transfer time"
                        }
                    },
                    "required": ["service_type", "room_number"]
                }
            },
            {
                "name": "get_menu_item",
                "description": "Fetches live details about a specific menu item including availability and current price.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item_name": {
                            "type": "string",
                            "description": "Name of the menu item"
                        }
                    },
                    "required": ["item_name"]
                }
            },
            {
                "name": "place_room_order",
                "description": "Places a food or beverage order for a guest room.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_number": {
                            "type": "string"
                        },
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "quantity": {"type": "integer"},
                                    "notes": {"type": "string"}
                                }
                            }
                        }
                    },
                    "required": ["room_number", "items"]
                }
            }
        ]
    }
]