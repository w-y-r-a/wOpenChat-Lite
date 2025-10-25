from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
import os
import sys
import re
sys.path.insert(1, os.getcwd())
from src.models.register_data import RegisterData
from src.utils.create_user_json import create_user_json
from src.utils.database import get_collection
from src.utils.unencode_and_hash import hash_password
from src.utils.jwt_token import create_jwt_token



def validate_password(password: str) -> JSONResponse | None:
    if len(password) < 8:
        return JSONResponse(
            {
                "error": "ValidationError",
                "error_description": "Password must be at least 8 characters long"
            },
            status_code=422,
        )

    if not re.search(r'[A-Z]', password):
        return JSONResponse(
            {
                "error": "ValidationError",
                "error_description": "Password must contain at least one uppercase letter"
            },
            status_code=422,
        )

    if not re.search(r'[a-z]', password):
        return JSONResponse(
            {
                "error": "ValidationError",
                "error_description": "Password must contain at least one lowercase letter"
            },
            status_code=422,
        )

    if not re.search(r'\d', password):
        return JSONResponse(
            {
                "error": "ValidationError",
                "error_description": "Password must contain at least one number"
            },
            status_code=422,
        )

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return JSONResponse(
            {
                "error": "ValidationError",
                "error_description": "Password must contain at least one special character"
            },
            status_code=422,
        )

def validate_email(email: str) -> JSONResponse | None:
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return JSONResponse(
            {
                "error": "ValidationError",
                "error_description": "Invalid email format"
            },
            status_code=422
        )


def validate_username(username: str) -> JSONResponse | None:
    if not 3 <= len(username) <= 30:
        return JSONResponse(
            {
                "error": "ValidationError",
                "error_description": "Username must be between 3 and 30 characters"
            },
            status_code=422,
        )

    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return JSONResponse(
            {
                "error": "ValidationError",
                "error_description": "Username can only contain letters, numbers, underscores, and hyphens"
            },
            status_code=422,
        )


async def register(data: RegisterData, request: Request):
    """
    Registers a new user by validating the provided credentials and returning a JWT token upon successful registration.
    Args:
        data: RegisterData object containing username, email, and password.
        request: FastAPI Request object to access request headers.
    """
    ip_addr = request.headers.get("CF-Connecting-IP") or request.headers.get("X-Forwarded-For") or request.client.host
    users = await get_collection("users")
    sessions = await get_collection("sessions")

    # fields from LoginData
    username = data.username
    email = data.email
    raw_password = data.password
    password = hash_password(raw_password)

    # Validate inputs
    validate_username(username)
    validate_email(email)
    validate_password(raw_password)

    if await users.find_one({"username": username}):
        return JSONResponse(
            {
                "error": "UserExistsError",
                "error_description": "Username already exists"
            },
            status_code=409,
        )

    # convert to JSON
    user_json = create_user_json(
        username=username,
        email=email,
        password=password,
        admin=False,
        enabled=True,
        created_at=datetime.now(timezone.utc),
    )

    await users.insert_one(user_json)
    sub = user_json["sub"]

    session_id = os.urandom(16).hex()
    refresh_token = os.urandom(32).hex()
    token_data = {"sub": username, "sid": session_id}

    token = create_jwt_token(token_data, request.headers.get("host", ""), exp=30)

    await sessions.insert_one(
        {
            "sub": username,
            "session_id": session_id,
            "ip_address": ip_addr,
            "refresh_token": refresh_token,
            "created_at": datetime.now(timezone.utc),
            "expires_at": datetime.now(timezone.utc) + timedelta(days=30),
        }
    )

    return JSONResponse(
        {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 1800,
            "refresh_token": refresh_token,
            "message": "User registered successfully"
        },
        status_code=201,
    )