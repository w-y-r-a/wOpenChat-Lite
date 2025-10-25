from fastapi import Request
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse
import os
import sys
sys.path.insert(1, os.getcwd())
from src.utils.database import get_collection
from src.utils.jwt_token import decode_jwt_token
from src.models.userinfo import UserInfo

async def get_user_info(request: Request, data: UserInfo):
    users = await get_collection("users")
    sessions = await get_collection("sessions")

    token = data.access_token

    try:
        decoded_token = decode_jwt_token(token)
    except ValueError as e:
        return JSONResponse(
            {"error": "InvalidToken", "error_description": str(e)},
            status_code=401
        )

    session = await sessions.find_one({"session_id": decoded_token["sid"]})

    if not session:
        return JSONResponse(
            {
                "error": "InvalidSession",
                "error_description": "The session is invalid or has expired."
            }, status_code=401
        )

    expires_at = session.get("expires_at")
    if not isinstance(expires_at, datetime):
        return JSONResponse(
            {
                "error": "InvalidSessionTimestamp",
                "error_description": "Session expiry timestamp is missing or invalid."
            }, status_code=401
        )

    # Ensure both datetimes are timezone-aware (UTC)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        return JSONResponse(
            {
                "error": "SessionExpired",
                "error_description": "The session has expired."
            }, status_code=401
        )

    user = await users.find_one({"sub": session["sub"]})

    if not user:
        return JSONResponse(
            {
                "error": "UserNotFound",
                "error_description": "The user associated with the session was not found."
            }, status_code=404
        )

    if user.get("enabled") is False:
        return JSONResponse(
            {
                "error": "UserDisabled",
                "error_description": "The user account is disabled."
            }, status_code=403
        )

    user_info = {
        "sub": user.get("sub"),
        "username": user.get("username"),
        "email": user.get("email"),
        "picture": user.get("picture"),
        "admin": user.get("admin", False),
        "created_at": user.get("created_at") if user.get("created_at") else None
    }

    return JSONResponse(user_info, status_code=200)