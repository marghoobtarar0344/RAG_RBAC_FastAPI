
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

from database.session import get_db
from database.models import UserDB, RoleDB

from schemas.auth import UserResponse
from schemas.profile import ProfileUpdate, ProfileRoleUpdate
from schemas.token import TokenData

from middleware.current_user import get_current_user
from common.roles import check_role

router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Endpoint to retrieve user profile


@router.get("/{user_id}", response_model=UserResponse)
async def get_profile(
    user_id: int,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if the user has permission to read the profile
    await check_role(user, "read", "profile", db)

    # Fetch the user from the database
    result = await db.execute(select(UserDB).filter(UserDB.id == user_id))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": db_user.id, "username": db_user.username, "roles": [role.name for role in db_user.roles]}

# Endpoint to update user profile


@router.put("/{user_id}", response_model=UserResponse)
async def update_profile(
    user_id: int,
    profile: ProfileUpdate,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if the user has permission to update the profile
    await check_role(user, "write", "profile", db)

    # Fetch the user from the database
    result = await db.execute(select(UserDB).filter(UserDB.id == user_id))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user details if provided
    if profile.username:
        db_user.username = profile.username
    if profile.password:
        db_user.password = pwd_context.hash(profile.password)

    await db.commit()
    await db.refresh(db_user)

    return {"id": db_user.id, "username": db_user.username, "roles": [role.name for role in db_user.roles]}

# Endpoint to add roles to a user


@router.put("/add_role/{user_id}", response_model=UserResponse)
async def add_roles_to_user(
    user_id: int,
    role_data: ProfileRoleUpdate,
    user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if the user has admin rights to modify roles
    await check_role(user, "admin", "profile", db)

    # Fetch the user along with their roles
    result = await db.execute(select(UserDB).filter(UserDB.id == user_id).options(joinedload(UserDB.roles)))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch existing roles from the database
    result = await db.execute(select(RoleDB).filter(RoleDB.name.in_(role_data.roles)))
    existing_roles = result.scalars().all()
    existing_role_names = {role.name for role in existing_roles}

    # Identify new roles that need to be created
    missing_roles = [
        role_name for role_name in role_data.roles if role_name not in existing_role_names]
    new_roles = [RoleDB(name=role_name) for role_name in missing_roles]

    # Add new roles to the DB
    db.add_all(new_roles)
    await db.flush()  # Ensure IDs are assigned

    # Append new roles to the user's existing roles
    db_user.roles.extend(existing_roles + new_roles)

    await db.commit()
    await db.refresh(db_user)

    return {
        "id": db_user.id,
        "username": db_user.username,
        "roles": [role.name for role in db_user.roles]
    }


# Endpoint to remove roles from a user
@router.put("/remove_roles/{user_id}", response_model=UserResponse)
async def remove_roles_from_user(
    user_id: int,
    role_data: ProfileRoleUpdate,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if the user has admin rights
    await check_role(user, "admin", "profile", db)

    # Fetch the user along with their roles
    result = await db.execute(select(UserDB).filter(UserDB.id == user_id).options(joinedload(UserDB.roles)))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove only roles that the user has
    db_user.roles = [
        role for role in db_user.roles if role.name not in role_data.roles]

    await db.commit()
    await db.refresh(db_user)

    return {
        "id": db_user.id,
        "username": db_user.username,
        "roles": [role.name for role in db_user.roles]
    }


# Endpoint to delete a user profile
@router.delete("/{user_id}")
async def delete_profile(
    user_id: int,
    user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if the user has admin rights
    await check_role(user, "admin", "profile", db)

    # Fetch the user from the database
    result = await db.execute(select(UserDB).filter(UserDB.id == user_id))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user profile
    await db.delete(db_user)
    await db.commit()

    return {"message": "User deleted successfully"}
