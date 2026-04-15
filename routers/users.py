from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from DataBase.dao import UserDAO
from schemas.schemas import UserRead, UserCreate
from core.asyncsession_maker import get_db

router = APIRouter(prefix="/users", tags=["Users"])


# 1. Отримати список усіх користувачів
@router.get("", response_model=List[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = await UserDAO.find_all(db)
    return users


# 2. Створити нового користувача
@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Додаємо запис у базу даних через DAO
    new_user = await UserDAO.add(db, user)
    return new_user


# 3. Отримати одного користувача за ID
@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserDAO.find_all(db)
    result = next((u for u in user if u.id == user_id), None)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено"
        )
    return result


# 4. Видалити користувача
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return {"message": f"Користувач {user_id} видалений (реалізуй метод delete в DAO)"}