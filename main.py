from fastapi import FastAPI
# Імпортуємо наші нові файли з папки routers
from routers import users, categories, products, profiles, orders

app = FastAPI(title="Магазин (Приклад) на FastAPI")

# Підключаємо роутери
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(profiles.router)
app.include_router(orders.router)