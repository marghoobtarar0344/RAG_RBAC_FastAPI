from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from schemas.auth import UserCreate, UserResponse, LoginRequest
from schemas.token import Token

from .crud import (
    register_user,
    authenticate_user,
    create_access_token
)


router = APIRouter()

# Create User


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):

    return await register_user(user, db)


# Login Endpoint
@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(request.username, request.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username, "roles": [
                                role.name for role in user.roles]})
    return {"access_token": token, "token_type": "bearer"}
