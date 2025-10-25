import os
from datetime import datetime, timedelta, timezone
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorCollection
from src.utils.jwt_token import create_jwt_token


async def create_session_and_token(
    sub: str,
    ip_addr: str,
    request: Request,
    sessions: AsyncIOMotorCollection,
    exp_days: int = 30,
    token_exp_minutes: int = 30
) -> dict:
    """
    Creates a new session in the database and generates a JWT token.
    
    Args:
        sub: The user's subject identifier
        ip_addr: The IP address of the request
        request: The FastAPI Request object
        sessions: The sessions collection from MongoDB
        exp_days: Number of days until session expires (default: 30)
        token_exp_minutes: Number of minutes until token expires (default: 30)
    
    Returns:
        dict: A dictionary containing access_token, token_type, expires_in, and refresh_token
    """
    session_id = os.urandom(16).hex()
    refresh_token = os.urandom(32).hex()
    token_data = {"sub": sub, "sid": session_id}

    token = create_jwt_token(token_data, request.headers.get("host", ""), exp=token_exp_minutes)

    await sessions.insert_one(
        {
            "sub": sub,
            "session_id": session_id,
            "ip_address": ip_addr,
            "refresh_token": refresh_token,
            "created_at": datetime.now(timezone.utc),
            "expires_at": datetime.now(timezone.utc) + timedelta(days=exp_days),
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": token_exp_minutes * 60,  # convert minutes to seconds
        "refresh_token": refresh_token
    }


def get_client_ip(request: Request) -> str:
    """
    Extracts the client IP address from the request.
    Checks Cloudflare, X-Forwarded-For, and client.host in order.
    
    Args:
        request: The FastAPI Request object
    
    Returns:
        str: The client IP address
    """
    return request.headers.get("CF-Connecting-IP") or request.headers.get("X-Forwarded-For") or request.client.host
