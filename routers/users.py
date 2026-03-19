from fastapi import APIRouter, HTTPException, status
from schemas.users import UserCreate

router = APIRouter(prefix="/users", tags=["users"])

# --- Емуляція бази даних (звичайний словник) ---
fake_db = {}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    user_id = len(fake_db) + 1
    user_data = user.model_dump()
    fake_db[user_id] = {"id": user_id, **user_data}
    return fake_db[user_id]


@router.get("/")
def get_all_users():
    return list(fake_db.values())


@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]


@router.put("/{user_id}")
def update_user(user_id: int, user_update: UserCreate):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")

    updated_data = user_update.model_dump()
    fake_db[user_id] = {"id": user_id, **updated_data}
    return fake_db[user_id]


@router.delete("/{user_id}")
def delete_user(user_id: int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_db[user_id]
    return {"message": "User deleted successfully"}