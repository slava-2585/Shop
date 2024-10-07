from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import insert, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from controllers.user import UserCRUD, authenticate_user, create_access_token
from hashing import Hash
from models.database import get_async_session
from models.models import User
from models.schemas import ShowUser, UserCreate, Token

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
)

@router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        user_crud = UserCRUD(session)
        user = await user_crud.create_user(
            email=body.email,
            hashed_password=Hash.get_password_hash(body.password),
            )
        return user


@router.get("/", response_model=ShowUser)
async def get_user(user_email: str, session: AsyncSession = Depends(get_async_session)) -> User:
    async with session.begin():
        user_crud = UserCRUD(session)
        user = await user_crud.get_user_by_email(user_email)
        if user is None:
            raise HTTPException(
                status_code=404, detail=f"User with email: {user_email} not found."
            )
        return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: AsyncSession = Depends(get_async_session)
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": user.is_admin, "user_id": user.id},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


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


