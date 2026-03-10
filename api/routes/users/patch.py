from fastapi import APIRouter

router = APIRouter()


@router.patch("/{user_id}")
def update_user(user_id: int):
    return {"message": "patch request sent", "user_id": user_id}
