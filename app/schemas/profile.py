from pydantic import BaseModel
from typing import List, Optional

class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    
class ProfileRoleUpdate(BaseModel):
    roles: Optional[List[str]] = None