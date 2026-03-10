from fastapi import APIRouter

router = APIRouter()


@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"message": "delete request sent", "user_id": user_id}
