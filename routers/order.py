from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import insert, select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user import get_payload_from_token
from models.database import get_async_session
from models.models import Product, Order, Cart, User
from models.schemas import (
    CartCreate,
    GetOrder,
    GetCart,
)
from send_email import send_email, convert_tuple

router = APIRouter(
    prefix="/order",
    tags=["Заказы"],
)


# def get_msg(from_addr, to_addr, subject, text_msg):
#     msg = MIMEMultipart()
#     msg['Subject'] = subject
#     msg['From'] = from_addr
#     msg['To'] = to_addr
#     msg.attach(MIMEText(text_msg, 'plain'))
#     return msg


@router.get("/{id}", response_model=list[GetCart])
async def get_detail_order_for_number(
    id_order: int, session: AsyncSession = Depends(get_async_session)
):
    # Выборка корзины по номеру заказа
    query = (
        select(
            Product.name,
            Cart.quantity,
            (Cart.quantity * Product.price).label("total_price"),
        )
        .select_from(Cart)
        .join(Product)
        .filter(Cart.id_order == id_order)
    )
    # print(str(query))
    result = await session.execute(query)
    return result.all()


@router.get("/", response_model=list[GetOrder])
async def get_all_order(session: AsyncSession = Depends(get_async_session)):
    # Выборка всех заказов
    # query = (
    #     select(Order.id, Order.dt, User.email).select_from(Order).join(User)
    # )
    # Выбор всех заказов со стоимостью
    query = (
        select(
            Order.id,
            Order.dt,
            (User.firstname + " " + User.lastname).label("Name"),
            func.sum(Cart.quantity * Product.price).label("summa"),
        )
        .select_from(User)
        .join(Order)
        .join(Cart)
        .join(Product)
        .group_by(Order.id, Order.dt, User.firstname, User.lastname)
    )
    result = await session.execute(query)
    return result.all()


@router.post("/")
async def create_order(
    new_order: list[CartCreate],
    payload: dict = Depends(get_payload_from_token),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = insert(Order).values({"user_id": payload.get("user_id")}).returning(Order.id)
    rezult = await session.execute(stmt)
    id_order = rezult.first()[0]
    await session.commit()
    for item in new_order:
        item = item.model_dump()
        stmt = insert(Cart).values(
            {
                "id_order": id_order,
                "id_product": item["id_product"],
                "quantity": item["quantity"],
            }
        )
        await session.execute(stmt)
        await session.commit()

    # Запрос деталей заказа для отправки на почту
    query = (
        select(
            Product.name,
            Cart.quantity,
            (Cart.quantity * Product.price).label("total_price"),
        )
        .select_from(Cart)
        .join(Product)
        .filter(Cart.id_order == id_order)
    )
    result = await session.execute(query)
    result = result.all()
    # print(result)
    str_send = convert_tuple(result)
    try:
        await send_email(payload.get("sub"), str_send, f"Order #{id_order}")
    except:
        print("Error send mail")
    return {"status": "success"}


@router.delete("/{id}")
async def delete_order(
    id_order: int,
    payload: dict = Depends(get_payload_from_token),
    session: AsyncSession = Depends(get_async_session),
):
    if payload.get("is_admin"):
        stmt = delete(Order).where(Order.id == id_order).returning(Order.id)
        rezult = await session.execute(stmt)
        if rezult.raw.rowcount == 1:
            await session.commit()
            return {"status": "success"}
        raise HTTPException(status_code=404, detail="Order not found")
    else:
        raise HTTPException(status_code=403, detail=f"Access denied.")
