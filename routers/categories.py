from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from DataBase.dao import CategoryDAO
from schemas.schemas import CategoryRead, CategoryCreate
from core.asyncsession_maker import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=List[CategoryRead])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryDAO.find_all(db)

@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    # Передаємо об'єкт схеми прямо в DAO
    return await CategoryDAO.add(db, category)