from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean)


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    unit_of_measurement = Column(String)


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dt = Column(TIMESTAMP, default=datetime.utcnow)


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    id_order = Column(Integer, ForeignKey("order.id"))
    id_product = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer, nullable=False)


# ----------------- Core

# metadata = MetaData()

# roles = Table(
#     "roles",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
# )


# users = Table(
#     "users",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, unique=True, index=True),
#     Column("password", String, nullable=False),
#     Column("is_active", Boolean, default=True),
#     Column("registered_at", DateTime, default=datetime.utcnow),
#     Column("is_admin", Boolean),
# )
#
#
# product = Table(
#     "product",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
#     Column("price", Float, nullable=False),
#     Column("unit_of_measurement", String),
# )
#
# order = Table(
#     "order",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("user_id", Integer, ForeignKey("users.id")),
#     Column("dt", TIMESTAMP, default=datetime.utcnow),
# )
#
# cart = Table(
#     "cart",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("id_order", Integer, ForeignKey("order.id")),
#     Column("id_product", Integer, ForeignKey("product.id")),
#     Column("quantity", Integer, nullable=False),
# )
