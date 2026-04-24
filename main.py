from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import users, categories, products, profiles, orders, authentication
from core.asyncsession_maker import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    import DataBase.models
    async with engine.begin() as conn:
        # Залиш тільки створення, drop_all вже не потрібен
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Магазин (Приклад) на FastAPI і Docker",
    lifespan=lifespan
)

# Підключаємо роутери
app.include_router(authentication.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(profiles.router)
app.include_router(orders.router)