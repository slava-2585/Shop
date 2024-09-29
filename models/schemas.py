from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, EmailStr
from sqlalchemy import TIMESTAMP


#---------------User
# class Roles(str, Enum):
#     admin = "is_admin"
#     user = "is_user"


# class ShowUserToken (BaseModel):
#     sub: int
#     email: EmailStr
#     is_admin: bool


class ShowUser (BaseModel):
    is_active: bool
    registered_at: datetime
    id: int
    email: EmailStr
    is_admin: bool


class UserCreate (BaseModel):
    email: EmailStr
    password: str
    #is_active: bool
    #registered_at: datetime
    #is_admin: bool


class Token (BaseModel):
    access_token: str
    token_type: str

# -------------Product


class Measurement(str, Enum):
    kilogram = "кг"
    liter = "литр"
    things = "шт"


class ProductCreate(BaseModel):

    name: str = Field(min_length=3)
    price: float = Field(ge=0)
    unit_of_measurement: Measurement


class ProductUpdate(BaseModel):

    name: str | None = Field(min_length=3)
    price: float | None
    unit_of_measurement: Measurement | None = None


class ProductGet(ProductCreate):

    id: int


# order


class OrderGet(BaseModel):

    id: int
    user_id: ShowUser
    dt: datetime


class CartCreate(BaseModel):

    id_product: int
    quantity: int


class CartGet(CartCreate):

    id: int
    id_order: OrderGet
    id_product: ProductGet

