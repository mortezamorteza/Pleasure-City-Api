from pydantic import BaseModel, Field
from typing import Optional


# =====================================
# USER SCHEMAS
# =====================================

class UserCreate(BaseModel):
    username: Optional[str] = Field(
        default=None,
        max_length=30
    )


class UserResponse(BaseModel):
    user_id: str
    username: Optional[str] = None
    created_at: str


# =====================================
# CONFESSION SCHEMAS
# =====================================

class ConfessionCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=5000
    )

    category: str = Field(
        default="general",
        max_length=50
    )


class ConfessionResponse(BaseModel):
    confession_id: str
    user_id: str
    content: str
    category: str
    created_at: str


# =====================================
# COMMENT SCHEMAS
# =====================================

class CommentCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=2000
    )

    confession_id: str


# =====================================
# REACTION SCHEMAS
# =====================================

class ReactionCreate(BaseModel):
    confession_id: str
    reaction_type: str = Field(
        max_length=20
    )


# =====================================
# CHAT SCHEMAS
# =====================================

class MessageCreate(BaseModel):
    receiver_id: str
    content: str = Field(
        min_length=1,
        max_length=4000
    )


class MessageResponse(BaseModel):
    message_id: str
    sender_id: str
    receiver_id: str
    content: str
    created_at: str
