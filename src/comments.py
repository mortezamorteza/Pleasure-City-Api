from fastapi import APIRouter
from schemas import CommentCreate

router = APIRouter(
    prefix="/api/comments",
    tags=["Comments"]
)


@router.post("/")
async def create_comment(data: CommentCreate):
    return {
        "status": "pending_database"
    }


@router.get("/{confession_id}")
async def get_comments(confession_id: str):
    return {
        "confession_id": confession_id,
        "comments": [],
        "status": "pending_database"
    }


@router.delete("/{comment_id}")
async def delete_comment(comment_id: str):
    return {
        "comment_id": comment_id,
        "status": "pending_database"
    }
