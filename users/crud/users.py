from typing import Dict

from models import User
from pydantic import EmailStr
from sqlalchemy import Row
from sqlalchemy import RowMapping
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


def row2dict(obj: Row | RowMapping) -> Dict:
    result = {}
    for key in obj.__annotations__.keys():
        result.setdefault(key, getattr(obj, key))
    return result


async def get_user_by_email(session: AsyncSession, email: EmailStr) -> Dict:
    stmt = select(User).where(User.email == email)
    result = (await session.execute(stmt)).scalars().first()
    return row2dict(result)
