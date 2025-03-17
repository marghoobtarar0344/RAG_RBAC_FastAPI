from pydantic import BaseModel
from typing import List

class UserResponse(BaseModel):
    id: int
    username: str
    roles: List[str]



