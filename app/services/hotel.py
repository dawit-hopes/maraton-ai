import json
import logging

from google import genai
from google.genai import errors as genai_errors
from google.genai import types

from app.core.config import settings
from app.services.tools import tools
from app.services.prompts import build_system_instruction_food

logger = logging.getLogger(__name__)

HOTEL_NAME = "Haile Hotels & Resorts Group"

PUBLIC_FALLBACK_MESSAGE = (
    "Unable to load a response. "
    "Please contact the front desk for assistance."
)

class HotelChatService:
    def __init__(self, hotel_name: str):
        self.hotel_context = self._load_hotel_context()
        self.food_context = self._load_food_context()
        self.services_context = self._load_services_context()
        self.travel_tips_context = self._load_travel_tips_context()
        self.amenities_context = self._load_amenities_context()
        self.local_area_context = self._load_local_area_context()
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.hotel_name = hotel_name
        self.sessions = {}

    def _load_hotel_context(self) -> str:
        with open(settings.HOTEL_DATA_PATH, "r") as f:
            return json.dumps(json.load(f), indent=2, ensure_ascii=False)

    def _load_food_context(self) -> str:
        with open(settings.FOOD_DATA_PATH, "r") as f:
            return json.dumps(json.load(f), indent=2, ensure_ascii=False)

    def _load_services_context(self) -> str:
        with open(settings.SERVICES_DATA_PATH, "r") as f:
            return json.dumps(json.load(f), indent=2, ensure_ascii=False)

    def _load_travel_tips_context(self) -> str:
        with open(settings.TRAVEL_TIPS_DATA_PATH, "r") as f:
            return json.dumps(json.load(f), indent=2, ensure_ascii=False)

    def _load_amenities_context(self) -> str:
        with open(settings.AMENITIES_DATA_PATH, "r") as f:
            return json.dumps(json.load(f), indent=2, ensure_ascii=False)

    def _load_local_area_context(self) -> str:
        with open(settings.LOCAL_AREA_DATA_PATH, "r") as f:
            return json.dumps(json.load(f), indent=2, ensure_ascii=False)

    def _get_or_create_session(self, session_id: str):
        """Retrieves an existing chat session or creates a new stateful session with live tools."""
        if session_id in self.sessions:
            return self.sessions[session_id]

        chat = self.client.aio.chats.create(
            model=settings.GEMINI_MODEL,
            config=types.GenerateContentConfig(
                system_instruction=build_system_instruction_food(
                    self.hotel_name,
                    self.food_context,
                    self.services_context,
                    self.travel_tips_context,
                    self.amenities_context,
                    self.local_area_context,
                    self.hotel_context,
                ),
                temperature=0.3,
                tools=tools,
            ),
        )

        self.sessions[session_id] = chat
        return chat

    async def stream_chat(self, user_message: str, session_id: str):
        """Streams conversation text while managing automated function calls natively."""
        if not settings.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is not configured")
            yield PUBLIC_FALLBACK_MESSAGE
            return


        try:
            chat_session = self._get_or_create_session(session_id)
            response_stream = await chat_session.send_message_stream(user_message)

            async for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
        except genai_errors.ClientError as error:
            logger.warning("Gemini API error (%s): %s", error.code, error)
            yield PUBLIC_FALLBACK_MESSAGE
        except Exception:
            logger.exception("Unexpected error during chat stream")
            yield PUBLIC_FALLBACK_MESSAGE

hotel_chat_service = HotelChatService(hotel_name=HOTEL_NAME)