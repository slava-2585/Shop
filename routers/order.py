from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import insert, select, update, delete
from sqlalchemy.dialects.postgresql import insert as insert_list
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_async_session
from models.models import product, order, cart
from models.schemas import ProductCreate, Product, ProductUpdate, CartCreate, Order

router = APIRouter(
    prefix="/order",
    tags=["Заказы"],
)


@router.get("/{id}", response_model=list[Order])
async def get_order(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(cart).where(cart.c.id_order == id)
    result = await session.execute(query)
    return result.all()


@router.post("/")
async def create_order(new_order: list[CartCreate], session: AsyncSession = Depends(get_async_session)):

    stmt = insert(order).values({"user_id": 1}).returning(order.c.id)
    rezult = await session.execute(stmt)
    id_order = rezult.first()[0]
    await session.commit()
    for item in new_order:
        item = item.dict()
        print(item)
        print(id_order)
        stmt = insert(cart).values({"id_order": id_order, "id_product": item["id_product"],
                                    "quantity": item["quantity"]})
        rezult = await session.execute(stmt)
        await session.commit()
    return {"status": "success"}