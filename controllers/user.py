# Отдельные функции и классы для работы с пользователями.
from datetime import datetime, timedelta, timezone
from typing import Union, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from config import settings
from hashing import Hash
from models.models import User


class UserCRUD:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self, email: str, hashed_password: str, firstname: str, lastname: str
    ) -> User:
        new_user = User(
            email=email,
            password=hashed_password,
            firstname=firstname,
            lastname=lastname,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: int) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]
        else:
            return None

    async def get_user_by_id(self, user_id: int) -> Union[User, None]:
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        query = select(User).where(User.email == email)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]


# Login Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


async def authenticate_user(
    email: str, password: str, session: AsyncSession
) -> Union[User, None]:

    # user = await _get_user_by_email_for_auth(email=email, session=db)
    user_crud = UserCRUD(session)
    user = await user_crud.get_user_by_email(email=email)

    if user is None:
        return None
    if Hash.verify_password(user.password, password):
        return user
    else:
        return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_payload_from_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error:"
        )
    return payload
