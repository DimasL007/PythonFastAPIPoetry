from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from jose import jwt, JWTError

from DataBase.dao import UserDAO
from schemas.schemas import UserRead, UserCreate
from core.asyncsession_maker import get_db
from core.config import settings
from cookies.manager import AUTH_COOKIE_NAME
from authentication.dependencies import get_current_user
from DataBase.models import User

router = APIRouter(prefix="/users", tags=["Users"])


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get(AUTH_COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Аккаунт не знайдено, увійдіть в систему"
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Невалідний токен")
    except JWTError:
        raise HTTPException(status_code=401, detail="Помилка авторизації")

    user = await UserDAO.find_one_or_none(db, id=int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Користувача не знайдено")

    return user


# --- ЕНДПОІНТИ (РУЧКИ) ---

@router.get("/me", response_model=UserRead)
async def read_me(user=Depends(get_current_user)):
    return user


@router.get("", response_model=List[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    # Тут краще додати перевірку на адміна, але для лаби ок
    users = await UserDAO.find_all(db)
    return users


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserDAO.find_one_or_none(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Користувача з ID {user_id} не знайдено"
        )
    return user


@router.delete("/me/delete")
async def delete_current_user(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    success = await UserDAO.delete(db, current_user.id)

    if not success:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    response = JSONResponse(content={"message": "Ваш аккаунт успішно видалено"})
    response.delete_cookie(AUTH_COOKIE_NAME)

    return response