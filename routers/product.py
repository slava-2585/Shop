from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_async_session
from models.models import product
from models.schemas import ProductCreate, Product, ProductUpdate

router = APIRouter(
    prefix="/product",
    tags=["Продукты"],
)


@router.get("/", response_model=list[Product])
async def get_product(session: AsyncSession = Depends(get_async_session)):
    query = select(product)
    result = await session.execute(query)
    return result.all()


@router.post("/")
async def create_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(product).values(**new_product.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.put("/{id}")
async def edit_product(id: int, new_product: ProductUpdate, session: AsyncSession = Depends(get_async_session)):
    stmt = update(product).where(product.c.id == id).values(**new_product.dict(exclude_unset=True)).returning(product.c.id)
    rezult = await session.execute(stmt)
    if rezult.rowcount == 1:
        await session.commit()
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/{id}")
async def delete_product(id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(product).where(product.c.id == id).returning(product.c.id)
    rezult = await session.execute(stmt)
    if rezult.rowcount == 1:
        await session.commit()
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Product not found")



