from oso import Oso
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.future import select

from database.models import UserDB
from schemas.token import TokenData


# Oso Setup
oso = Oso()
oso.load_files(["policy.polar"])
# Check Role in Oso (async)
async def check_role(user: TokenData, action: str, resource: str, db: AsyncSession):
    print('it is checking the roles')
    result = await db.execute(select(UserDB).filter(UserDB.username == user.username))
    user_db = result.scalars().first()
    if not user_db:
        raise HTTPException(status_code=403, detail="User not found")
    
    roles = [role.name for role in user_db.roles]  # Extract role names as strings
    print('it is checking the roles ==>',roles,action,resource)
    if oso.is_allowed({"name": user_db.username, "roles": roles}, action, resource):
        return True

    raise HTTPException(status_code=403, detail=f"Permission denied role is {roles} action is {action}")
