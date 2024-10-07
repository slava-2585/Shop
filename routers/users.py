from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import insert, select, delete, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from controllers.user import UserCRUD, authenticate_user, create_access_token, get_payload_from_token
from hashing import Hasher, Hash
from models.database import get_async_session
from models.models import User
from models.schemas import ShowUser, UserCreate, Token, UpdateUser

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
            firstname=body.firstname,
            lastname=body.lastname,
            )
        return user


@router.get("/", response_model=ShowUser)
async def get_user(user_email: str,
                    payload: dict = Depends(get_payload_from_token),
                   session: AsyncSession = Depends(get_async_session)) -> User:
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
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password, user inactive",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": user.is_admin, "user_id": user.id},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/{id}")
async def delete_user(user_id: int,
                    payload: dict = Depends(get_payload_from_token),
                    session: AsyncSession = Depends(get_async_session)):
    if payload.get('is_admin'):
        async with session.begin():
            user_crud = UserCRUD(session)
            del_user_is = await user_crud.delete_user(user_id)
            if del_user_is is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            else:
                return {"Delete user is id": del_user_is}
    else:
        raise HTTPException(status_code=403, detail=f"Access denied.")


@router.patch("/", response_model=ShowUser)
async def update_user(
                            body: UpdateUser,
                            session: AsyncSession = Depends(get_async_session),
                            payload: dict = Depends(get_payload_from_token),
                            ):
    user_id = payload.get("user_id")
    query = (
        update(User)
        .where(and_(User.id == user_id, User.is_active == True))
        .values(firstname=body.firstname, lastname=body.lastname)
        .returning(User)
    )
    res = await session.execute(query)
    update_user = res.fetchone()
    if update_user is not None:
        return update_user[0]