import asyncio

import yaml
from sqlalchemy import insert, bindparam

from config import settings
from hashing import Hash
from models.database import async_session_maker
from models.models import Product, User


# session: AsyncSession = get_async_session()
async def dataimport():
    async with async_session_maker() as session:
        with open("Shop.yaml", encoding="utf-8") as sh:
            read_data = yaml.safe_load(sh)
            query_user = insert(User).values(
                firstname="admin",
                lastname="admin",
                email=settings.ADMINMAIL,
                password=Hash.get_password_hash(settings.ADMINPASS),
                is_admin=True,
            )
            query = insert(Product).values(
                name=bindparam("name"),
                price=bindparam("price"),
                unit_of_measurement=bindparam("unit_of_measurement"),
                characteristics=bindparam("characteristics"),
                description=bindparam("description"),
            )
            await session.execute(query, read_data)
            await session.execute(query_user)
            await session.commit()


asyncio.run(dataimport())
