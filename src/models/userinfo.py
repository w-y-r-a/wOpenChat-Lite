from pydantic import BaseModel

class UserInfo(BaseModel):
    access_token: str