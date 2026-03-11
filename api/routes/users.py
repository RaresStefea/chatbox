from typing import Optional
from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from api.services import users as users_service
from db.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return users_service.get_all_users(db)


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return users_service.get_user(db, user_id)


@router.post("/")
def create_user(
    email: str = Body(...),
    name: Optional[str] = Body(None),
    db: Session = Depends(get_db),
):
    return users_service.create_user(db, email=email, name=name)


@router.patch("/{user_id}")
def update_user(user_id: int, data: dict = Body(...), db: Session = Depends(get_db)):
    return users_service.update_user(db, user_id, data)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return users_service.delete_user(db, user_id)
