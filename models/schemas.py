from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


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
    price: float
    unit_of_measurement: measurement


class Product(BaseModel):

    id: int
    name: str
    price: float
    unit_of_measurement: measurement


