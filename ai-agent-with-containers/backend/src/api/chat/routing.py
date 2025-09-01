from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session
from .models import ChatMessagePayload, ChatMessage, ChatMessageList, ChatMessageListItem
from api.db import get_session

router = APIRouter()

@router.get("/chat")
def read_chat():
    return {"message": "This is the chat endpoint"}

@router.get("/")
def chat_health():
    return {"status": "Chat API ok"}

# /api/chats/recent
@router.get("/recent", response_model=List[ChatMessageListItem])
def chat_get_recent_messages(
    limit: int = 10,
    session: Session = Depends(get_session)
):
    messages = session.query(ChatMessage).order_by(ChatMessage.id.desc()).limit(limit).all()
    return messages


# curl -X POST -d '{"message": "Hello, World!"}' -H "Content-Type: application/json" http://localhost:3002/api/chats/
@router.post("/", response_model=ChatMessage)
def chat_create_message(
    payload:ChatMessagePayload,
    session: Session = Depends(get_session)
):
    data = payload.model_dump() # pydantic -> dict
    print("Received chat message payload:", data)
    new_message = data.get("message")
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj) # ensure id/primar key is populated   
    return obj
    return {"message": "Create chat message endpoint"}