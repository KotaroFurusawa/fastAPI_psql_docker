from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, token
from ..database import get_db
from ..hashing import Hash
from .. import oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Auth']
)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invalid Credentials')

    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Incorrect password')

    access_token = token.create_access_token(
        data={"sub": user.email, "id": user.id}
    )

    refresh_token = token.create_refresh_token(
        data={"sub": user.email, "id": user.id}, db=db
    )

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}


@router.get("/refresh")  # ここで送られるトークンにはrefreshトークンを設定(front)
async def refresh_token(
        current_user=Depends(oauth2.get_current_user_with_refresh_token),
        db: Session = Depends(get_db)):
    """リフレッシュトークンでトークンを再取得"""
    access_token = token.create_access_token(
        data={"sub": current_user.email, "id": current_user.id}
    )

    refresh_token = token.create_refresh_token(
        data={"sub": current_user.email, "id": current_user.id}, db=db
    )

    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"}
