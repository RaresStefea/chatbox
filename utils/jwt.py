import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv

# TIP: load_env should always run before trying to access the env vars so it gets injected and the os can retrieve it
if os.getenv("ENV") != "production":
    load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY missing, check env vars.")

ALGORITHM = "HS256"
EXPIRE_MINUTES = 60 * 24


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": int(expire.timestamp())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return payload
    except (jwt.JWTError, ValueError):
        return None
