from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .token import verify_token

from sqlalchemy.orm import Session
from .database import get_db

# トークンを発行するエンドポイントを引数に
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"www-Authenticate": "Bearer"}
    )

    result = verify_token(token, credentials_exception, db, mode="ACCESS")
    return {result}


def get_current_user_with_refresh_token(token: str = Depends(oauth2_scheme),
                                        db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"www-Authenticate": "Bearer"}
    )

    result = verify_token(token, credentials_exception, db, mode="REFRESH")
    return {result}
