"""
Chat API routes.
Handles conversation endpoints for the chatbot.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
sys.path.append('..')
from services.chat_service import process_chat_message

router = APIRouter(prefix="/chat", tags=["chat"])


class Message(BaseModel):
    """Single chat message."""
    role: str  # 'user' or 'assistant'
    content: str


class ChatRequest(BaseModel):
    """Chat request payload."""
    message: str
    conversation_history: Optional[List[Message]] = None


class ChatResponse(BaseModel):
    """Chat response payload."""
    response: str
    intent: str
    sources: dict


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return AI response.

    The system will:
    1. Analyze the query intent (semantic vs structured)
    2. Search the database using appropriate methods
    3. Generate a contextual response using GPT
    """
    try:
        # Convert history to list of dicts if provided
        history = None
        if request.conversation_history:
            history = [{"role": m.role, "content": m.content} for m in request.conversation_history]

        result = process_chat_message(request.message, history)

        return ChatResponse(
            response=result["response"],
            intent=result["intent"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "chat"}
