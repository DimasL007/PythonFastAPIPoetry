from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

# --- Схеми для User ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # <--- ДОДАЙ ЦЕЙ РЯДОК

class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Схеми для UserProfile (зв'язок 1:1) ---
class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    user_id: int

class UserProfileCreate(UserProfileBase):
    pass

class UserProfileRead(UserProfileBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Схеми для Category ---
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Схеми для Product ---
class ProductBase(BaseModel):
    title: str
    price: int
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- Схеми для Order ---
class OrderBase(BaseModel):
    status: str = "pending"
    user_id: int

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True