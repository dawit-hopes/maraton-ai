import json

from app.services.pricing import get_room_quote


def check_room_availability(location: str, room_type: str, guests_count: int = 2) -> str:
    """
    Checks real-time room availability and pricing details for a specific Haile Resort destination.

    Args:
        location: The resort city (e.g., 'Hawassa', 'Arba Minch', 'Ziway', 'Gondar', 'Addis Ababa', 'Adama')
        room_type: Type of room (e.g., 'Standard', 'Deluxe', 'Suite', 'Family Room')
        guests_count: Number of guests staying.
    """
    return json.dumps(get_room_quote(location, room_type, guests_count), ensure_ascii=False)
