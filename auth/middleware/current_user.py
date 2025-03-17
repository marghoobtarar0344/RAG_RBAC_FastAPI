from fastapi import Depends, HTTPException, status
from schemas.token import TokenData
from jose import jwt, JWTError
from fastapi.security import HTTPBearer
from config.global_variables import (
    SECRET_KEY,
    ALGORITHM
)
security = HTTPBearer()


# Dependency: Get Current User from JWT (async)
async def get_current_user(token: str = Depends(security)):
    try:
        token = token.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(username=payload.get("sub"), roles=payload.get("roles"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
