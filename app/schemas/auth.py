from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str
    roles: List[str]

class UserResponse(BaseModel):
    id: int
    username: str
    roles: List[str]

class LoginRequest(BaseModel):
    username: str
    password: str

