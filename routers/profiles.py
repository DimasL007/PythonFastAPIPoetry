from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from DataBase.dao import UserProfileDAO
from schemas.schemas import UserProfileRead, UserProfileCreate
from core.asyncsession_maker import get_db

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.get("", response_model=List[UserProfileRead])
async def get_all_profiles(db: AsyncSession = Depends(get_db)):
    return await UserProfileDAO.find_all(db)

@router.post("", response_model=UserProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile(profile: UserProfileCreate, db: AsyncSession = Depends(get_db)):
    return await UserProfileDAO.add(db, **profile.model_dump())