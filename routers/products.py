from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from DataBase.dao import ProductDAO
from schemas.schemas import ProductRead, ProductCreate
from core.asyncsession_maker import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=List[ProductRead])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    return await ProductDAO.find_all(db)

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    return await ProductDAO.add(db, **product.model_dump())