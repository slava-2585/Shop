from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base


class Roles(Base):
    __tablename__ = "roles",
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("roles.id")),


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    unit_of_measurement = Column(String)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dt = Column(TIMESTAMP, default=datetime.utcnow)


class Cart(Base):
    __tablename = "carts"

    id = Column(Integer, primary_key=True)
    id_order = Column(Integer, ForeignKey("orders.id"))
    id_product = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
