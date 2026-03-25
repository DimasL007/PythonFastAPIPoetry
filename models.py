from typing import List, Optional
from sqlalchemy import ForeignKey, String, BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from asyncsession_maker import Base


# 1. Модель Користувача (User)
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Зв'язок 1:1 з профілем (One-to-One)
    # uselist=False робить цей зв'язок саме одиничним
    profile: Mapped["UserProfile"] = relationship(back_populates="user", uselist=False)

    # Зв'язок 1:M з замовленнями (One-to-Many)
    orders: Mapped[List["Order"]] = relationship(back_populates="user")


# 2. Модель Профілю (UserProfile) - Зв'язок 1:1
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(100))
    bio: Mapped[Optional[str]] = mapped_column(Text)

    # Зовнішній ключ на юзера
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="profile")


# 3. Модель Категорії (Category) - Зв'язок 1:M з товарами
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # У одній категорії може бути багато товарів
    products: Mapped[List["Product"]] = relationship(back_populates="category")


# 4. Модель Товару (Product)
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[int] = mapped_column()  # Ціна в копійках/центах для точності

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")


# 5. Модель Замовлення (Order) - Зв'язок 1:M з User
class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="orders")