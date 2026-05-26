import json
from google import genai
from google.genai import types
from app.core.config import settings

HOTEL_NAME = "Haile Hotels & Resorts Group"

class GeminiChatService:
    def __init__(self, hotel_name: str):
        self.hotel_context = self._load_hotel_context()
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.hotel_name = hotel_name
        self.sessions = {}

    def _load_hotel_context(self) -> str:
        with open(settings.HOTEL_DATA_PATH, "r") as f:
            return json.dumps(json.load(f), indent=2, ensure_ascii=False)

    def _get_or_create_session(self, session_id: str):
        """Retrieves an existing chat session or creates a new stateful session."""
        if session_id in self.sessions:
            return self.sessions[session_id]
        
        system_instruction = (
            f"You are a warm, highly detailed, and proactive digital concierge chatbot for {self.hotel_name}. "
            "Your goal is to answer guest questions comprehensively using the provided hotel details.\n\n"
            
            "CRITICAL BEHAVIOR RULES:\n"
            "1. DETAILED RESPONSES: Provide deep, thorough information. Do not give short summaries.\n"
            "2. PROACTIVE ENGAGEMENT: Always end your response with an open-ended, helpful follow-up question related to the guest's inquiry.\n"
            "3. ONLINE BOOKING RULE: If the guest asks about booking a room, checking availability, or pricing, explicitly tell them: "
            "'Please use the online booking system directly on our website to book your stay.' Do not tell them to call the front desk for bookings.\n"
            "4. MEMORY AWARENESS: This is an ongoing continuous conversation. Do NOT repeat greeting phrases like 'Welcome to Haile Hotels & Resorts!' "
            "or introduce yourself again if you have already greeted the guest in a previous turn.\n"
            "5. FRONT DESK FALLBACK: Only refer the guest to the front desk as an absolute last resort if their question is completely missing from the data.\n\n"
            
            f"Hotel Details and Knowledge Base:\n{self.hotel_context}"
        )

        # Create a persistent chat session using the asynchronous client
        chat = self.client.aio.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.4,
            ),
        )
        
        self.sessions[session_id] = chat
        return chat

    async def stream_chat(self, user_message: str, session_id: str):
        """Streams conversation text while maintaining user session memory."""
        chat_session = self._get_or_create_session(session_id)
        
        # Use send_message_stream to naturally retain past conversation history
        response_stream = await chat_session.send_message_stream(user_message)

        async for chunk in response_stream:
            if chunk.text:
                yield chunk.text

gemini_chat_service = GeminiChatService(hotel_name=HOTEL_NAME)