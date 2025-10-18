import json
from typing import Optional, Any
from uuid import uuid4
import datetime

def create_user_json(username: str, email: str, password: str, admin: Optional[bool], enabled: bool, created_at) -> \
dict[str, str | bool | None | Any]:
    json_data =  {
        "sub": str(uuid4()),
        "username": username,
        "email": email,
        "password": password,
        "admin": admin,
        "enabled": enabled,
        "created_at": created_at,
    }
    return json_data