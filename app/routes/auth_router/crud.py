
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import RoleDB, UserDB


from config.global_variables import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Authenticate & Generate JWT (async)
async def authenticate_user(username: str, password: str, db: AsyncSession):
    result = await db.execute(select(UserDB).filter(UserDB.username == username))
    user = result.scalars().first()
    if not user or not pwd_context.verify(password, user.password):
        return None
    return user


#  Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Register userasync def register_user(user, db: AsyncSession):
async def register_user(user, db: AsyncSession ):
    hashed_password = pwd_context.hash(user.password)

    # Fetch existing roles
    result = await db.execute(select(RoleDB).filter(RoleDB.name.in_(user.roles)))
    existing_roles = result.scalars().all()

    # Create new roles if they don't exist
    new_roles = []
    for role_name in user.roles:
        if not any(role.name == role_name for role in existing_roles):
            new_role = RoleDB(name=role_name)
            db.add(new_role)
            print('append role')
            new_roles.append(new_role)

    await db.flush()  # Ensure roles get IDs
    all_roles = existing_roles + new_roles

    # Create user
    db_user = UserDB(username=user.username, password=hashed_password)
    db_user.roles = all_roles
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return {"id": db_user.id, "username": db_user.username, "roles": [role.name for role in db_user.roles]}