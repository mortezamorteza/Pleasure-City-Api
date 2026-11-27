from fastapi import APIRouter

router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)


@router.get("/")
async def get_notifications():
    return {
        "status": "pending_database",
        "notifications": []
    }


@router.get("/unread")
async def get_unread_notifications():
    return {
        "status": "pending_database",
        "count": 0
    }


@router.post("/{notification_id}/read")
async def mark_as_read(notification_id: str):
    return {
        "notification_id": notification_id,
        "status": "pending_database"
    }
