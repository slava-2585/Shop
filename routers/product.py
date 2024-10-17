# Модуль для работы с товарами. Создание удаление и изменение
from fastapi import APIRouter, Depends, HTTPException
from fastapi_filters import FilterValues, create_filters
from fastapi_filters.ext.sqlalchemy import apply_filters

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user import get_payload_from_token
from models.database import get_async_session
from models.models import Product
from models.schemas import ProductCreate, GetProduct, ProductUpdate

router = APIRouter(
    prefix="/product",
    tags=["Продукты"],
)


@router.get("/", response_model=list[GetProduct]) # доступно с обычными правами
async def get_product(
    session: AsyncSession = Depends(get_async_session),
    payload: dict = Depends(get_payload_from_token),
    filters: FilterValues = Depends(create_filters(price=float)),
):
    query = apply_filters(select(Product), filters)
    result = await session.scalars(query)
    return result.all()


@router.post("/") # Доступно с правами админа
async def create_product(
    new_product: ProductCreate,
    payload: dict = Depends(get_payload_from_token),
    session: AsyncSession = Depends(get_async_session),
):
    if payload.get("is_admin"):
        stmt = insert(Product).values(**new_product.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    else:
        raise HTTPException(status_code=403, detail=f"Access denied.")


@router.patch("/{id}") # Доступно с правами админа
async def edit_product(
    id_product: int,
    new_product: ProductUpdate,
    payload: dict = Depends(get_payload_from_token),
    session: AsyncSession = Depends(get_async_session),
):
    if payload.get("is_admin"):
        stmt = (
            update(Product)
            .where(Product.id == id_product)
            .values(**new_product.model_dump(exclude_unset=True))
            .returning(Product.id)
        )
        rezult = await session.execute(stmt)
        if rezult.raw.rowcount == 1:
            await session.commit()
            return {"status": "success"}
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        raise HTTPException(status_code=403, detail=f"Access denied.")


@router.delete("/{id}") # Доступно с правами админа
async def delete_product(
    id_product: int,
    payload: dict = Depends(get_payload_from_token),
    session: AsyncSession = Depends(get_async_session),
):
    if payload.get("is_admin"):
        stmt = delete(Product).where(Product.id == id_product).returning(Product.id)
        rezult = await session.execute(stmt)
        if rezult.raw.rowcount == 1:
            await session.commit()
            return {"status": "success"}
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        raise HTTPException(status_code=403, detail=f"Access denied.")
