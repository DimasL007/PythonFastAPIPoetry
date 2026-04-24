from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.models import User, Product, Category, Order, UserProfile

class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, session: AsyncSession):
        result = await session.execute(select(cls.model))
        return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        result = await session.execute(select(cls.model).filter_by(**filter_by))
        return result.scalars().first()

    @classmethod
    async def add(cls, session: AsyncSession, **data):
        new_instance = cls.model(**data)
        session.add(new_instance)
        await session.commit()
        await session.refresh(new_instance)
        return new_instance

    @classmethod
    async def delete(cls, session: AsyncSession, user_id: int):
        query = select(cls.model).filter_by(id=user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user:
            await session.delete(user)
            await session.commit()
            return True
        return False

class UserDAO(BaseDAO):
    model = User

class ProductDAO(BaseDAO):
    model = Product

class CategoryDAO(BaseDAO):
    model = Category

class OrderDAO(BaseDAO):
    model = Order

class UserProfileDAO(BaseDAO):
    model = UserProfile