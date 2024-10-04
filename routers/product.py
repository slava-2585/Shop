from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.user import get_payload_from_token
from models.database import get_async_session
from models.models import Product
from models.schemas import ProductCreate, ProductGet, ProductUpdate
from send_email import send_email

router = APIRouter(
    prefix="/product",
    tags=["Продукты"],
)


@router.get("/", response_model=list[ProductGet])
async def get_product(session: AsyncSession = Depends(get_async_session)):
    query = select(Product)
    result = await session.scalars(query)
    return result.all()


@router.post("/")
async def create_product(
        new_product: ProductCreate,
        payload: dict = Depends(get_payload_from_token),
        session: AsyncSession = Depends(get_async_session)
):
    if payload.get('is_admin'):
        stmt = insert(Product).values(**new_product.dict())
        await session.execute(stmt)
        await session.commit()
        return {"status": "success"}
    else:
        raise HTTPException(
            status_code=403, detail=f"Access denied."
        )


@router.put("/{id}")
async def edit_product(id: int, new_product: ProductUpdate,
                       payload: dict = Depends(get_payload_from_token),
                       session: AsyncSession = Depends(get_async_session)
                       ):
    if payload.get('is_admin'):
        stmt = update(Product).where(Product.id == id).values(**new_product.dict(exclude_unset=True)).returning(Product.id)
        rezult = await session.execute(stmt)
        if rezult.rowcount == 1:
            await session.commit()
            return {"status": "success"}
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        raise HTTPException(status_code=403, detail=f"Access denied.")


@router.delete("/{id}")
async def delete_product(id: int,
                         payload: dict = Depends(get_payload_from_token),
                         session: AsyncSession = Depends(get_async_session)
                         ):
    if payload.get('is_admin'):

        stmt = delete(Product).where(Product.id == id).returning(Product.id)
        rezult = await session.execute(stmt)
        if rezult.raw.rowcount==1:
            await session.commit()
            return {"status": "success"}
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        raise HTTPException(status_code=403, detail=f"Access denied.")



