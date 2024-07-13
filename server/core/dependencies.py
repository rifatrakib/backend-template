from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from server.core.connections import get_database_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        session: AsyncSession = get_database_session()
        yield session
    finally:
        await session.close()
