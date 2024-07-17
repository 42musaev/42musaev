from typing import Dict

from models.refresh_session import RefreshSession
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


async def refresh_session_create(session: AsyncSession, data: Dict) -> int:
    stmt = insert(RefreshSession).values(**data).returning(RefreshSession.id)
    result = await session.scalar(stmt)
    await session.commit()
    return result
