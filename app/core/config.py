import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    HOTEL_DATA_PATH: str = "app/data/hotel_data.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()