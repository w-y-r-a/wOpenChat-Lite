from pydantic import BaseModel

class RegisterData(BaseModel):
    username: str
    email: str
    password: str
