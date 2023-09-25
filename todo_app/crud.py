from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
import models, schemas, utils

def create_todo(db:Session,todo:schemas.TodoCreate,current_user):
    db_todo = models.Todo(user_id=current_user.id,**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_all(db:Session,current_user):
    todos=db.query(models.Todo).filter(current_user.id == models.Todo.user_id).all()
    return todos

def get_one(db:Session,todo_id : int,current_user):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404,detail='No such Todo')
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403,detail='Not authorized to perform requested action')
    return db_todo  

def delete_todo(db:Session,todo_id:int,current_user):
    db_todo_query=db.query(models.Todo).filter(models.Todo.id == todo_id)
    db_todo=db_todo_query.first()
    if db_todo is None:
        raise HTTPException(status_code=404,detail='Todo not Found')
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403,detail='Not authorized to perform requested action')
    db_todo_query.delete(synchronize_session=False)
    db.commit()

    return {'Message' : 'Todo was deleted successfuly'}

def update_todo(db:Session,todo_id:int,post:schemas.TodoCreate,current_user):
    db_todo_query=db.query(models.Todo).filter(models.Todo.id == todo_id)
    db_todo=db_todo_query.first()
    if db_todo is None:
        raise HTTPException(status_code=404,detail='No such Todo')
    db_todo_query.update(post.dict(),synchronize_session=False)
    db.commit()
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403,detail='Not authorize to perform requested action')
    return db_todo

def create_user(db:Session,user:schemas.UserCreate):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db:Session,user_email:EmailStr):
    db_user = db.query(models.User).filter(models.User.email == user_email).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail=f'user with email: {user_email} not found')
    return db_user