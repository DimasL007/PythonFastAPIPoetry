from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from DataBase.dao import OrderDAO
from schemas.schemas import OrderRead, OrderCreate
from core.asyncsession_maker import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("", response_model=List[OrderRead])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    return await OrderDAO.find_all(db)

@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    return await OrderDAO.add(db, order)