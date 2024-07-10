from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import insert, select, update, delete
from sqlalchemy.dialects.postgresql import insert as insert_list
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_async_session
from models.models import Product, Order, Cart
from models.schemas import ProductCreate, ProductGet, ProductUpdate, CartCreate, OrderGet

router = APIRouter(
    prefix="/order",
    tags=["Заказы"],
)

def get_msg(from_addr, to_addr, subject, text_msg):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg.attach(MIMEText(text_msg, 'plain'))
    return msg


@router.get("/{id}", response_model=list[OrderGet])
async def get_order(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Cart).where(Cart.id_order == id)
    result = await session.execute(query)
    # Выборка корзины по номеру заказа
    query1 = (select([Product.name,
                      Cart.quantity,
                      (Cart.quantity * Product.price).label("price")]).
              select_from(Cart.join(Product))).where(Cart.id_order == id)
    return result.all()


@router.post("/")
async def create_order(new_order: list[CartCreate], session: AsyncSession = Depends(get_async_session)):

    stmt = insert(OrderGet).values({"user_id": 1}).returning(OrderGet.id)
    rezult = await session.execute(stmt)
    id_order = rezult.first()[0]
    await session.commit()
    for item in new_order:
        item = item.dict()
        print(item)
        print(id_order)
        stmt = insert(Cart).values({"id_order": id_order, "id_product": item["id_product"],
                                    "quantity": item["quantity"]})
        rezult = await session.execute(stmt)
        await session.commit()
    return {"status": "success"}