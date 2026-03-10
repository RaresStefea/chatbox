from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_users():
    return {"message": "get request sent"}


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"message": "get request sent", "user_id": user_id}
