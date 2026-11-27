from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import hashlib
import secrets

from database import fetch_one, fetch_all, execute_query

router = APIRouter(prefix="/users", tags=["Users"])

==============================

MODELS

==============================

class RegisterUser(BaseModel):
username: str
email: Optional[str] = None
password: str

class UpdateProfile(BaseModel):
username: Optional[str] = None
email: Optional[str] = None
avatar: Optional[str] = None
bio: Optional[str] = None

class ChangePassword(BaseModel):
old_password: str
new_password: str

==============================

PASSWORD

==============================

def hash_password(password: str):
salt = secrets.token_hex(16)

hashed = hashlib.sha256(
    (salt + password).encode("utf-8")
).hexdigest()

return salt + ":" + hashed

def verify_password(password: str, stored: str):
try:
salt, hashed = stored.split(":", 1)

    check = hashlib.sha256(
        (salt + password).encode("utf-8")
    ).hexdigest()

    return secrets.compare_digest(check, hashed)

except Exception:
    return False

==============================

REGISTER

==============================

@router.post("/register")
async def register_user(data: RegisterUser, request: Request):

username = data.username.strip()
email = data.email.strip().lower() if data.email else None

if len(username) < 3:
    raise HTTPException(400, "Username is too short")

if len(data.password) < 8:
    raise HTTPException(400, "Password must be at least 8 characters")

existing = await fetch_one(
    request,
    "SELECT id FROM users WHERE username = ?",
    username
)

if existing:
    raise HTTPException(409, "Username already exists")

if email:
    existing_email = await fetch_one(
        request,
        "SELECT id FROM users WHERE email = ?",
        email
    )

    if existing_email:
        raise HTTPException(409, "Email already exists")

password_hash = hash_password(data.password)

await execute_query(
    request,
    """
    INSERT INTO users (username, email, password)
    VALUES (?, ?, ?)
    """,
    username,
    email,
    password_hash
)

user = await fetch_one(
    request,
    """
    SELECT id, username, email, avatar, bio, created_at
    FROM users
    WHERE username = ?
    """,
    username
)

return {
    "success": True,
    "message": "Registration successful",
    "user": user
}

==============================

GET USER PROFILE

==============================

@router.get("/{user_id}")
async def get_user(user_id: int, request: Request):

user = await fetch_one(
    request,
    """
    SELECT id, username, avatar, bio, created_at
    FROM users
    WHERE id = ? AND is_active = 1
    """,
    user_id
)

if not user:
    raise HTTPException(404, "User not found")

return {
    "success": True,
    "user": user
}

==============================

SEARCH USERS

==============================

@router.get("/search/{username}")
async def search_users(username: str, request: Request):

users = await fetch_all(
    request,
    """
    SELECT id, username, avatar, bio
    FROM users
    WHERE username LIKE ? AND is_active = 1
    LIMIT 20
    """,
    "%" + username + "%"
)

return {
    "success": True,
    "users": users
}

==============================

UPDATE PROFILE

==============================

@router.put("/{user_id}")
async def update_profile(
user_id: int,
data: UpdateProfile,
request: Request
):

user = await fetch_one(
    request,
    "SELECT id FROM users WHERE id = ? AND is_active = 1",
    user_id
)

if not user:
    raise HTTPException(404, "User not found")

updates = data.model_dump(exclude_unset=True)

if not updates:
    raise HTTPException(400, "No data provided")

if "username" in updates:
    updates["username"] = updates["username"].strip()

    if len(updates["username"]) < 3:
        raise HTTPException(400, "Username is too short")

    duplicate = await fetch_one(
        request,
        "SELECT id FROM users WHERE username = ? AND id != ?",
        updates["username"],
        user_id
    )

    if duplicate:
        raise HTTPException(409, "Username already exists")

if "email" in updates and updates["email"]:
    updates["email"] = updates["email"].strip().lower()

    duplicate = await fetch_one(
        request,
        "SELECT id FROM users WHERE email = ? AND id != ?",
        updates["email"],
        user_id
    )

    if duplicate:
        raise HTTPException(409, "Email already exists")

allowed = ["username", "email", "avatar", "bio"]

fields = [key for key in updates if key in allowed]

if not fields:
    raise HTTPException(400, "Invalid fields")

query = "UPDATE users SET " + ", ".join(
    key + " = ?" for key in fields
) + " WHERE id = ?"

values = [updates[key] for key in fields]
values.append(user_id)

await execute_query(request, query, *values)

return {
    "success": True,
    "message": "Profile updated"
}

==============================

CHANGE PASSWORD

==============================

@router.put("/{user_id}/password")
async def change_password(
user_id: int,
data: ChangePassword,
request: Request
):

user = await fetch_one(
    request,
    "SELECT password FROM users WHERE id = ? AND is_active = 1",
    user_id
)

if not user:
    raise HTTPException(404, "User not found")

if not verify_password(
    data.old_password,
    user["password"]
):
    raise HTTPException(400, "Incorrect old password")

if len(data.new_password) < 8:
    raise HTTPException(400, "New password is too short")

new_hash = hash_password(data.new_password)

await execute_query(
    request,
    "UPDATE users SET password = ? WHERE id = ?",
    new_hash,
    user_id
)

return {
    "success": True,
    "message": "Password changed"
}

==============================

DEACTIVATE ACCOUNT

==============================

@router.delete("/{user_id}")
async def deactivate_account(user_id: int, request: Request):

user = await fetch_one(
    request,
    "SELECT id FROM users WHERE id = ?",
    user_id
)

if not user:
    raise HTTPException(404, "User not found")

await execute_query(
    request,
    "UPDATE users SET is_active = 0 WHERE id = ?",
    user_id
)

return {
    "success": True,
    "message": "Account deactivated"
}
