from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from typing import Dict
import os
import sys
sys.path.insert(1, os.getcwd())
from src.settingsmanager import read_config

SECRET_KEY = read_config().get("secret_key")

def create_jwt_token(data: dict, host: str, exp: Optional[int]) -> str:
    """
    Creates a JWT token with given data and a user set expiration time.
    Args:
        exp (int): Expiration time in minutes.(If None, defaults to 30 minutes)
        data (dict): The data to encode in the JWT token.
        host (str): The "Host" header accessed via the FastAPI request(or really just anything but mainly that).
    Returns:
        str: The encoded JWT token.
    """
    if exp is None:
        exp = 30  # Default expiration time in minutes

    expiration = datetime.now(timezone.utc) + timedelta(minutes=exp)

    to_encode = data.copy()
    to_encode.update({
        "exp": expiration,
        "iat": datetime.now(timezone.utc),
        "iss": host
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def decode_jwt_token(token: str) -> Dict:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")