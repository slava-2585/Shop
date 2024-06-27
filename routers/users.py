from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_async_session
from models.models import roles
from models.schemas import AddRoles, Roles

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


@router.get("/", response_model=list[Roles])
async def get_roles(roles_name: str, session: AsyncSession = Depends(get_async_session)):
    query = select(roles).where(roles.c.name == roles_name)
    result = await session.execute(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Roles not found")
    return result.all()


@router.post("/")
async def add_roles(new_operation: AddRoles, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(roles).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
