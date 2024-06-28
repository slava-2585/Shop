from fastapi import FastAPI

from routers.users import router as user_router
from routers.product import router as product_router
from routers.order import router as order_router

app = FastAPI(
    title="Spare parts store"
)

app.include_router(order_router)
app.include_router(product_router)
app.include_router(user_router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
