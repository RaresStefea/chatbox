from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.repositories import users_DELETE as users_repo

# Aici se pune si logica de encryptare a parolei/validare


def get_all_users(db: Session):
    return users_repo.get_all(db)


def get_user(db: Session, user_id: int):
    user = users_repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(db: Session, email: str, name: Optional[str] = None):
    return users_repo.create(db, email=email, name=name)


def update_user(db: Session, user_id: int, data: dict):
    user = users_repo.update(db, user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def delete_user(db: Session, user_id: int):
    user = users_repo.delete(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
