from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import TIMESTAMP


class Roles(BaseModel):
    id: int
    name: str


class AddRoles(BaseModel):
    name: str


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

    name: str
    price: float = Field(ge=0)
    unit_of_measurement: measurement


class ProductUpdate(BaseModel):

    name: str | None = None
    price: float | None = None
    unit_of_measurement: measurement | None = None


class Product(BaseModel):

    id: int
    name: str
    price: float
    unit_of_measurement: measurement


# order


class Order(BaseModel):

    id: int
    user_id: User
    dt: datetime


class Order(BaseModel):

    id: int
    id_order: int
    id_product: int
    quantity: int


class CartCreate(BaseModel):

    #id_order: Order
    id_product: int
    quantity: int
