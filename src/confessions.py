from fastapi import APIRouter
from schemas import ConfessionCreate

router = APIRouter(
    prefix="/api/confessions",
    tags=["Confessions"]
)


@router.post("/")
async def create_confession(data: ConfessionCreate):
    return {
        "status": "pending_database",
        "message": "Confession received"
    }


@router.get("/")
async def get_confessions():
    return {
        "status": "pending_database",
        "confessions": []
    }


@router.get("/{confession_id}")
async def get_confession(confession_id: str):
    return {
        "confession_id": confession_id,
        "status": "pending_database"
    }


@router.delete("/{confession_id}")
async def delete_confession(confession_id: str):
    return {
        "status": "pending_database",
        "confession_id": confession_id
    }
