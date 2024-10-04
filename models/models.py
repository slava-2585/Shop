from datetime import datetime
from typing import Annotated

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base, str_256


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    registered_at: Mapped[created_at]
    is_admin: Mapped[bool] = mapped_column(default=False)

    order: Mapped[list["Order"]] = relationship(back_populates="user")


class Product(Base):
    __tablename__ = "product"

    id: Mapped[intpk]
    name: Mapped[str]
    price: Mapped[float]
    unit_of_measurement: Mapped[str]


class Order(Base):
    __tablename__ = "order"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    dt: Mapped[created_at]

    user: Mapped["User"] = relationship(back_populates="order")


class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[intpk]
    id_order: Mapped[int] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"))
    id_product: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"))
    quantity: Mapped[float] = mapped_column(nullable=False)
