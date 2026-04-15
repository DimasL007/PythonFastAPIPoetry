import asyncio
from asyncsession_maker import async_session_maker # Виправили імпорт тут
from models import User, UserProfile, Category, Product, Order

async def seed():
    async with async_session_maker() as session:
        # 1. Створюємо користувача
        user = User(username="User1_admin", email="Email@example1.com")
        session.add(user)
        await session.flush() # Отримуємо ID користувача без комміту

        # 2. Створюємо профіль (1:1)
        profile = UserProfile(full_name="Programist1", bio="Student1", user_id=user.id)
        session.add(profile)

        # 3. Створюємо категорію
        cat = Category(name="Laptop1")
        session.add(cat)
        await session.flush()

        # 4. Створюємо товар (1:M)
        prod = Product(title="Gaming Laptop1", price=500100, category_id=cat.id)
        session.add(prod)

        # 5. Приклад замовлення
        new_order = Order(
            user_id=user.id,
            status="completed"
        )
        session.add(new_order)

        await session.commit()
        print("✅ Дані успішно додані в усі таблиці!")

if __name__ == "__main__":
    asyncio.run(seed())