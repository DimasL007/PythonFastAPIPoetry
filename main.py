from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from asyncsession_maker import get_db # Твоя фабрика сесій
from schemas import UserRead, UserCreate
from dao import UserDAO
from schemas import OrderRead

from schemas import ProductRead, ProductCreate, CategoryRead, CategoryCreate, OrderRead, OrderCreate, UserProfileRead, UserProfileCreate
from dao import ProductDAO, CategoryDAO, OrderDAO, UserProfileDAO


app = FastAPI()

@app.get("/users", response_model=List[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await UserDAO.find_all(db)

@app.post("/users", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserDAO.add(db, username=user.username, email=user.email)

@app.get("/categories", response_model=list[CategoryRead])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryDAO.find_all(db)

@app.post("/categories", response_model=CategoryRead)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await CategoryDAO.add(db, category)

# --- ТОВАРИ ---
@app.get("/products", response_model=list[ProductRead])
async def get_products(db: AsyncSession = Depends(get_db)):
    return await ProductDAO.find_all(db)

@app.post("/products", response_model=ProductRead)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await ProductDAO.add(db, product)

# --- ПРОФІЛІ ---
@app.get("/profiles", response_model=list[UserProfileRead])
async def get_profiles(db: AsyncSession = Depends(get_db)):
    return await UserProfileDAO.find_all(db)

# --- ЗАМОВЛЕННЯ (Orders) ---
@app.get("/orders", response_model=list[OrderRead])
async def get_orders(db: AsyncSession = Depends(get_db)):
    return await OrderDAO.find_all(db)

@app.post("/orders", response_model=OrderRead)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    # Передаємо дані у форматі словника для DAO
    return await OrderDAO.add(db, order)

# --- ПРОФІЛІ (User Profiles) ---
@app.get("/profiles", response_model=list[UserProfileRead])
async def get_profiles(db: AsyncSession = Depends(get_db)):
    return await UserProfileDAO.find_all(db)

@app.post("/profiles", response_model=UserProfileRead)
async def create_profile(profile: UserProfileCreate, db: AsyncSession = Depends(get_db)):
    return await UserProfileDAO.add(db, profile)