from fastapi import APIRouter


router = APIRouter()

@router.get("/chat")
def read_chat():
    return {"message": "This is the chat endpoint"}

@router.get("/")
def chat_health():
    return {"status": "Chat API ok"}