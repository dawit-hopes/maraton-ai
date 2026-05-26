from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.gemini import gemini_chat_service


router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return StreamingResponse(
        gemini_chat_service.stream_chat(request.message, request.session_id),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache"},
    )