from fastapi import APIRouter
from schemas import ReactionCreate

router = APIRouter(
    prefix="/api/reactions",
    tags=["Reactions"]
)


@router.post("/")
async def add_reaction(data: ReactionCreate):
    return {
        "status": "pending_database"
    }


@router.get("/{confession_id}")
async def get_reactions(confession_id: str):
    return {
        "confession_id": confession_id,
        "reactions": {},
        "status": "pending_database"
    }


@router.delete("/{confession_id}")
async def remove_reaction(confession_id: str):
    return {
        "confession_id": confession_id,
        "status": "pending_database"
    }
