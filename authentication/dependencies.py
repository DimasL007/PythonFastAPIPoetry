from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from core.config import settings
from DataBase.dao import UserDAO
from core.asyncsession_maker import get_db
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    # 1. Дістаємо токен з куки (назва має збігатися з AUTH_COOKIE_NAME у твоєму менеджері)
    token = request.cookies.get("shop_access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Ви не авторизовані (токен відсутній)")

    try:
        # 2. Декодуємо токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Невалідний токен")
    except JWTError:
        raise HTTPException(status_code=401, detail="Помилка токена")

    # 3. Шукаємо юзера в базі
    user = await UserDAO.find_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Користувача не знайдено")

    return user