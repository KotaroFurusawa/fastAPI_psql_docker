from typing import Optional
from . import models
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .functions.user import show

SECRET_KEY = "secret"  # 外部ファイルから引っ張ってくる
JWT_REFRESH_SECRET_KEY = "refresh"  # 外部ファイルから引っ張ってくる
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, db: Session,
                         expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    # リフレッシュトークンをdbに保存
    user = db.query(models.User).filter(models.User.id == data["id"]).first()
    user.refreshToken = encoded_jwt
    db.commit()

    return encoded_jwt


def verify_token(token: str, credentials_exception, db: Session, mode: str):
    try:
        payload = jwt.decode(token,  SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        id: int = payload.get("id")
        user = show(id, db)
        if email is None:
            raise credentials_exception
        if mode == "REFRESH" and user.refreshToken != token:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user
