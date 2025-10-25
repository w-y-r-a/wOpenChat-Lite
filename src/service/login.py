from fastapi import Request
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse
from bcrypt import checkpw
import os
import sys
sys.path.insert(1, os.getcwd())
from src.models.login_data import LoginData
from src.utils.database import get_collection
from src.utils.unencode_and_hash import hash_password
from src.utils.jwt_token import create_jwt_token


async def login(data: LoginData, request: Request) -> JSONResponse:
    ip_addr = request.headers.get("CF-Connecting-IP") or request.headers.get("X-Forwarded-For") or request.client.host
    users = await get_collection("users")
    sessions = await get_collection("sessions")

    email = data.email
    raw_password = data.password
    hashed_password = hash_password(raw_password) # to compare with stored hashed password
    try:
        user = await users.find_one({"email": email})
    except KeyError:
        return JSONResponse(
            {
                "error": "UserNotFound"
            }, status_code=404,
        )

    if user.get("enabled") is False:
        return JSONResponse(
            {
                "error": "UserDisabled",
                "error_description": "The user account is disabled."
            }, status_code=403
        )

    stored_hashed_password = user.get("password")
    if isinstance(stored_hashed_password, str):
        stored_hashed_password = stored_hashed_password.encode()

    if not checkpw(raw_password.encode(), stored_hashed_password):
        return JSONResponse({"error": "WrongPassword"}, status_code=401)

    # prepare to create session and token

    sub = user.get("sub")

    session_id = os.urandom(16).hex()
    refresh_token = os.urandom(32).hex()
    token_data = {"sub": sub, "sid": session_id}

    token = create_jwt_token(token_data, request.headers.get("host", ""), exp=30)

    await sessions.insert_one(
        {
            "sub": sub,
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
            "refresh_token": refresh_token
        }, status_code=200
    )