import json
from functools import lru_cache

from app.core.config import settings


@lru_cache
def load_pricing_data() -> dict:
    with open(settings.ROOM_PRICING_PATH, "r") as f:
        return json.load(f)


def _normalize_location(location: str) -> str:
    loc = location.lower().strip()
    aliases = {
        "arbaminch": "arba minch",
        "arba-minch": "arba minch",
        "addis": "addis ababa",
        "bole": "addis ababa",
    }
    return aliases.get(loc, loc)


def _match_room_type(room_types: dict, room_type: str) -> str:
    query = room_type.lower().strip()
    for name in room_types:
        if name.lower() in query or query in name.lower():
            return name
    return next(iter(room_types))


def _format_etb(amount: int) -> str:
    return f"{amount:,} ETB"


def resolve_location_key(location: str) -> str:
    loc = _normalize_location(location)
    locations = load_pricing_data()["locations"]
    return next((key for key in locations if key in loc or loc in key), "hawassa")


def get_room_quote(location: str, room_type: str, guests_count: int = 2) -> dict:
    pricing = load_pricing_data()
    location_key = resolve_location_key(location)
    location_data = pricing["locations"][location_key]
    room_types = location_data["room_types"]
    matched_room = _match_room_type(room_types, room_type)
    room = room_types[matched_room]

    if guests_count > room["max_guests"]:
        return {
            "status": "Capacity Exceeded",
            "resort": location_data["display_name"],
            "room_type": matched_room,
            "max_guests": room["max_guests"],
            "requested_guests": guests_count,
            "suggestion": f"Consider a Family Room or Suite, or book multiple {matched_room} rooms.",
        }

    if not room["available"]:
        alternative = room.get("alternative", "Deluxe")
        alt_room = room_types.get(alternative)
        alt_rate = _format_etb(alt_room["rates"]["weekday"]) if alt_room else None
        return {
            "status": "Fully Booked",
            "resort": location_data["display_name"],
            "room_type": matched_room,
            "alternative": f"{alternative} Room is available from {alt_rate} per night." if alt_rate else None,
        }

    weekday_rate = room["rates"]["weekday"]
    weekend_rate = room["rates"]["weekend"]
    return {
        "status": "Available",
        "resort": location_data["display_name"],
        "city": location_data["city"],
        "room_type": matched_room,
        "max_guests": room["max_guests"],
        "bed_configuration": room["bed_configuration"],
        "view": room["view"],
        "rate_per_night_weekday": _format_etb(weekday_rate),
        "rate_per_night_weekend": _format_etb(weekend_rate),
        "rate_per_night_peak_season_from": _format_etb(room["rates"]["peak_weekday"]),
        "features": (
            f"{room['view']}, {room['bed_configuration']}, breakfast included, "
            "free access to swimming pool and health club."
        ),
        "notes": pricing["pricing_notes"][:2],
    }
