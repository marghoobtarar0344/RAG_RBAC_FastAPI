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

# Endpoint for user registration


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Calls the function to create and store a new user in the database
    return await register_user(user, db)


# Login Endpoint
@router.post("/login", response_model=Token)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    # Authenticates the user by checking username and password
    user = await authenticate_user(request.username, request.password, db)
    if not user:
        # Raises an exception if authentication fails
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Generates a JWT access token with user roles
    token = create_access_token({"sub": user.username, "roles": [
                                role.name for role in user.roles]})
    # Returns the generated token
    return {"access_token": token, "token_type": "bearer"}
