from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, EmailStr


# ---------User------------


class User(BaseModel):
    email: EmailStr
    firstname: str = Field(min_length=3)
    lastname: str = Field(min_length=3)


class UserCreate(User):
    password: str


class ShowUser(User):
    id: int
    is_active: bool
    registered_at: datetime
    is_admin: bool


class UpdateUser(BaseModel):
    firstname: str | None = None
    lastname: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


# -------------Product----------------


class Measurement(str, Enum):
    kilogram = "кг"
    liter = "литр"
    things = "шт"


class ProductCreate(BaseModel):

    name: str = Field(min_length=3)
    price: float = Field(ge=0)
    unit_of_measurement: Measurement
    characteristics: str | None
    description: str | None


class ProductUpdate(BaseModel):

    name: str | None = Field(min_length=3)
    price: float | None
    unit_of_measurement: Measurement | None = None
    characteristics: str | None = None
    description: str | None = None


class GetProduct(ProductCreate):

    id: int


# order


class GetOrder(BaseModel):

    id: int
    dt: datetime
    Name: str
    Summa: float


class CartCreate(BaseModel):

    id_product: int
    quantity: int


class GetCart(BaseModel):
    name: str
    quantity: float
    total_price: float
