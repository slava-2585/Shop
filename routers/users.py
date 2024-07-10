from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_async_session
from models.schemas import AddRoles, Roles



router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)


# @router.get("/roles/", response_model=list[Roles])
# async def get_roles(roles_name: str, session: AsyncSession = Depends(get_async_session)):
#     query = select(roles).where(roles.c.name == roles_name)
#     result = await session.execute(query)
#     if result is None:
#         raise HTTPException(status_code=404, detail="Roles not found")
#     return result.all()
#
#
# @router.post("/roles/")
# async def create_roles(new_operation: AddRoles, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(roles).values(**new_operation.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}
#
#
# @router.put("/roles/{id}")
# async def edit_roles(id: int, new_roles: AddRoles, session: AsyncSession = Depends(get_async_session)):
#     stmt = update(roles).where(roles.c.id == id).values(**new_roles.dict(exclude_unset=True)).returning(roles.c.id)
#     rezult = await session.execute(stmt)
#     if rezult.rowcount == 1:
#         await session.commit()
#         return {"status": "success"}
#     raise HTTPException(status_code=404, detail="Product not found")
#
#
# @router.delete("/roles/{id}")
# async def delete_roles(id: int, session: AsyncSession = Depends(get_async_session)):
#     stmt = delete(roles).where(roles.c.id == id).returning(roles.c.id)
#     rezult = await session.execute(stmt)
#     print(rezult.rowcount)
#     if rezult.rowcount == 1:
#         await session.commit()
#         return {"status": "success"}
#     raise HTTPException(status_code=404, detail="Product not found")