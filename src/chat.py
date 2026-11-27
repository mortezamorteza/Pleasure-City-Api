from fastapi import APIRouter
from schemas import MessageCreate

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


@router.post("/send")
async def send_message(data: MessageCreate):
    return {
        "status": "pending_database"
    }


@router.get("/messages/{user_id}")
async def get_messages(user_id: str):
    return {
        "user_id": user_id,
        "messages": [],
        "status": "pending_database"
    }


@router.get("/conversations")
async def get_conversations():
    return {
        "status": "pending_database",
        "conversations": []
    }
