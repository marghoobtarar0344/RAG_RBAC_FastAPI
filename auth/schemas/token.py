from pydantic import BaseModel
from typing import List


class TokenData(BaseModel):
    username: str
    roles: List[str]

class Token(BaseModel):
    access_token: str
    token_type: str
