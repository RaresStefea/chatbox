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


def create_access_token(data) -> str:
    payload = data.model_dump()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
