from fastapi import APIRouter
from fastapi import Depends
from db.models import UserRecord
from db.database import get_db
from pydantic import BaseModel, Field, EmailStr

router = APIRouter(prefix="/auth", tags=["auth"])


class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=5, max_length=20)
    avatar_url: str = Field(default="")
    password_hash: str = Field(min_length=8, max_length=20)


class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    avatar_url: str
    password_hash: str


class TokenResponse(BaseModel):
    user: User
    access_token: str
    token_type: str = "bearer"


@router.post("/login")
def login():
    pass


@router.post("/signup", response_model=TokenResponse)
def signup(user_create: UserCreate, db=Depends(get_db)):

    # TODO: create hash_password function
    hashed_pass = "testhash"  # hash the password

    new_user = UserRecord(
        email=user_create.email,
        name=user_create.name,
        avatar_url=user_create.avatar_url,
        password_hash=hashed_pass,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user = User(
        id=new_user.id,
        email=new_user.email,
        name=new_user.name,
        avatar_url=new_user.avatar_url or "",
        password_hash=new_user.password_hash or "",
    )
    # TODO:
    # - read about JWT tokens
    # - implement create_access_token
    access_token = "test"  # create_access_token(data=user) JWT

    # TODO: return nice error if user already exists

    return TokenResponse(user=user, access_token=access_token)
