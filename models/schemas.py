from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import TIMESTAMP


class AddRoles(BaseModel):
    name: str


class Roles(AddRoles):
    id: int


class User (BaseModel):
    id: int
    email: str
    password: str
    is_active: bool
    registered_at: datetime
    role_id: Roles


class UserCreate (BaseModel):
    email: str
    password: str
    is_active: bool
    registered_at: datetime
    role_id: Roles

# -------------Product


class measurement(str, Enum):
    kilogram = "кг"
    liter = "литр"
    things = "шт"


class ProductCreate(BaseModel):

    name: str = Field(min_length=3)
    price: float = Field(ge=0)
    unit_of_measurement: measurement


class ProductUpdate(BaseModel):

    name: str | None = Field(min_length=3)
    price: float | None
    unit_of_measurement: measurement | None = None


class Product(ProductCreate):

    id: int


# order


class Order(BaseModel):

    id: int
    user_id: User
    dt: datetime


class CartCreate(BaseModel):

    id_product: int
    quantity: int


class Cart(CartCreate):

    id: int
    id_order: Order
    id_product: Product

