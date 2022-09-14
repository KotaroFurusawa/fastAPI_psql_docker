from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from .schemas import TokenData
from sqlalchemy.orm import Session
from .functions.user import show

SECRET_KEY = "secret"  # 外部ファイルから引っ張ってくる
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception, db: Session):
    try:
        payload = jwt.decode(token,  SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        id: int = payload.get("id")
        if email is None:
            raise credentials_exception
    except JWTError:
        credentials_exception
    user = show(id, db)
    return user
