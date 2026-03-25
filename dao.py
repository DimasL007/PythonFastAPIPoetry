from sqlalchemy.future import select
from models import User, Product, Category, Order, UserProfile

# Базовий клас для повторення логіки (щоб не писати одне і те ж)
class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, session):
        result = await session.execute(select(cls.model))
        return result.scalars().all()

    @classmethod
    async def add(cls, session, data):
        new_instance = cls.model(**data.model_dump())
        session.add(new_instance)
        await session.commit()
        await session.refresh(new_instance)
        return new_instance



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