from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.asyncsession_maker import get_db
from authentication.hash_logic import hash_password, verify_password
from JWT.token_handler import create_access_token
from cookies.manager import set_auth_cookie
from DataBase.dao import UserDAO
from schemas.schemas import UserCreate

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED )
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_exists = await UserDAO.find_one_or_none(db, email=user_data.email)

    if user_exists:
        raise HTTPException(status_code=409, detail="Email вже зайнятий")

    hashed_pwd = hash_password(user_data.password)

    # ДОДАНО username=user_data.username
    await UserDAO.add(
        db,
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    return {"status": "success", "message": "Ви успішно зареєстровані"}


@router.post("/login")
async def login(response: Response, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await UserDAO.find_one_or_none(db, email=user_data.email)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Невірний логін або пароль")

    token = create_access_token({"sub": str(user.id)})
    set_auth_cookie(response, token)

    return {"message": "Вхід виконано"}