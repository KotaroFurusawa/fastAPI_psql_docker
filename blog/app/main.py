from fastapi import FastAPI, Depends, status, Response, HTTPException
from .schemas import Blog, ShowBlog, User, ShowUser
from typing import List
from .models import Base
from . import models
from .database import engine, sessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/blog', response_model=List[ShowBlog])
def all_fetch(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(blog: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title, body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=ShowBlog)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'BLog with the id {id} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'BLog with the id {id} is not available'}
    return blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'BLog with the id {id} is not available')

    blog.delete(synchronize_session=False)
    db.commit()

    return 'Deletion completed'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'BLog with the id {id} is not available')
    blog.update(request.dict())
    db.commit()
    return 'Update completed'


@app.post('/user')
def create_user(request: User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email,
        password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')
    return user
