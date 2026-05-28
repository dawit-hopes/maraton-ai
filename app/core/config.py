import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    HOTEL_DATA_PATH: str = "app/data/hotel_data.json"
    FOOD_DATA_PATH: str = "app/data/food_data.json"
    ROOM_PRICING_PATH: str = "app/data/room_pricing.json"
    SERVICES_DATA_PATH: str = "app/data/service_data.json"
    TRAVEL_TIPS_DATA_PATH: str = "app/data/travel_tips.json"
    AMENITIES_DATA_PATH: str = "app/data/amenities_data.json"
    LOCAL_AREA_DATA_PATH: str = "app/data/local_area_data.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()