from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase  # НОВИЙ РЯДОК
from config import settings

engine = create_async_engine(settings.database_url)

# НОВИЙ КЛАС - це фундамент для твоїх моделей
class Base(DeclarativeBase):
    pass

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as session:
        yield session