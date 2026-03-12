from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.models import UserRecord
from db.database import get_db
from api.models import LoginRequest, SignupRequest, TokenResponse, UserResponse
from utils import security, jwt

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
def signup(body: SignupRequest, db: Session = Depends(get_db)):

    if db.query(UserRecord).filter(UserRecord.email == body.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered!"
        )

    user = UserRecord(
        email=body.email,
        name=body.name,
        password_hash=security.hash_password(body.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return TokenResponse(
        access_token=jwt.create_access_token(user.id),
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserRecord).filter(UserRecord.email == body.email).first()

    if (
        not user
        or not user.password_hash
        or not security.verify_password(body.password, user.password_hash)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password!",
        )

    return TokenResponse(
        access_token=jwt.create_access_token(user.id),
        user=UserResponse.model_validate(user),
    )
