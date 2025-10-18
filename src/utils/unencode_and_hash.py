import base64
import bcrypt
from typing import Union


def unencode(data: bytes) -> str:
    """
    Decode base64-encoded bytes to a UTF-8 string.
    """
    decoded_bytes = base64.b64decode(data)
    return decoded_bytes.decode("utf-8")


def hash_password(value: Union[str, bytes]) -> str:
    """
    Hash a string or bytes using bcrypt and return the hashed password as a UTF-8 string.
    """
    if isinstance(value, str):
        value_bytes = value.encode("utf-8")
    else:
        value_bytes = value
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(value_bytes, salt).decode("utf-8")