from fastapi import FastAPI
from routers.users import router as users_router

app = FastAPI()

# Підключаємо тільки те, що реально існує
app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "Hello User! Server is running!"}