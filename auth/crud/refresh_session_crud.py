from typing import Dict

from models.refresh_session import RefreshSession
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


async def refresh_session_create(session: AsyncSession, data: Dict) -> int:
    stmt = insert(RefreshSession).values(**data).returning(RefreshSession.id)
    result = await session.scalar(stmt)
    await session.commit()
    return result


async def update_refresh_session(
    session: AsyncSession, fingerprint: str, data: Dict
) -> int:
    stmt = (
        update(RefreshSession)
        .where(RefreshSession.fingerprint == fingerprint)
        .values(**data)
        .returning(RefreshSession.id)
    )
    result = await session.scalar(stmt)
    await session.commit()
    return result


async def get_refresh_session_id(session: AsyncSession, fingerprint: str) -> int | None:
    stmt = select(RefreshSession).where(RefreshSession.fingerprint == fingerprint)
    result = await session.execute(stmt)
    return result.scalar_one_or_none().id
