from fastapi import APIRouter, Depends

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_async_session
from models.models import product
from models.schemas import ProductCreate, Product

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
async def add_product(new_product: ProductCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(product).values(**new_product.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

