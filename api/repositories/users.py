from typing import Optional
from sqlalchemy.orm import Session

from db.models import UserRecord


def get_all(db: Session):
    return db.query(UserRecord).all()


def get_by_id(db: Session, user_id: int):
    return db.query(UserRecord).filter(UserRecord.id == user_id).first()


def create(db: Session, email: str, name: Optional[str] = None):
    user = UserRecord(email=email, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, user_id: int, data: dict):
    user = get_by_id(db, user_id)
    if not user:
        return None
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user_id: int):
    user = get_by_id(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user
