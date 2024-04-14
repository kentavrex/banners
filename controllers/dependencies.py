from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.db import SQLDBRepository
from repositories.sql import SessionLocal


async def get_async_db_session() -> AsyncSession:
    db = SessionLocal()
    yield db
    await db.close()


async def get_sql_db_repository(async_db_session: AsyncSession = Depends(get_async_db_session)):
    yield SQLDBRepository(async_db_session)
