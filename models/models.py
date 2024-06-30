from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData


metadata = MetaData()

# roles = Table(
#     "roles",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String, nullable=False),
# )


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, index=True),
    Column("password", String, nullable=False),
    Column("is_active", Boolean, default=True),
    Column("registered_at", DateTime, default=datetime.utcnow),
    Column("is_admin", Boolean),
)


product = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("price", Float, nullable=False),
    Column("unit_of_measurement", String),
)

order = Table(
    "order",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("dt", TIMESTAMP, default=datetime.utcnow),
)

cart = Table(
    "cart",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("id_order", Integer, ForeignKey("order.id")),
    Column("id_product", Integer, ForeignKey("product.id")),
    Column("quantity", Integer, nullable=False),
)
