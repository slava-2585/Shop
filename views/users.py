from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_async_session


def get_users(session: AsyncSession = Depends(get_async_session)):
    pass
