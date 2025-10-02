import json
from typing import Optional
from uuid import uuid4

def create_user_json(username: str, email: str, password: str, admin: Optional[bool], enabled: bool) -> dict:
    json_data =  {
        "sub": str(uuid4()),
        "username": username,
        "email": email,
        "password": password,
        "admin": admin,
        "enabled": enabled
    }
    json.dumps(json_data, indent=4)
    return json_data