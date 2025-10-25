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
from src.utils.session import create_session_and_token, get_client_ip


async def login(data: LoginData, request: Request) -> JSONResponse:
    ip_addr = get_client_ip(request)
    users = await get_collection("users")
    sessions = await get_collection("sessions")

    email = data.email
    raw_password = data.password
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

    session_token_data = await create_session_and_token(
        sub=sub,
        ip_addr=ip_addr,
        request=request,
        sessions=sessions
    )

    return JSONResponse(session_token_data, status_code=200)