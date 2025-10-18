import jwt
from datetime import datetime, timedelta, timezone
from src.settingsmanager import read_config, ensure_config, write_config

SECRET_KEY = read_config().get("secret_key")

def create_jwt_token(data: dict, host: str) -> str:
    """
    Creates a JWT token with given data and a 30-minute expiration time.
    Args:
        data (dict): The data to encode in the JWT token.
        host (str): The "Host" header accessed via the FastAPI request(or really just anything but mainly that).
    Returns:
        str: The encoded JWT token.
    """
    expiration = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode = data.copy()
    to_encode.update({
        "exp": expiration,
        "iat": datetime.now(timezone.utc),
        "iss": host
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")