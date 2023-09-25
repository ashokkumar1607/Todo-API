from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import EmailStr
import crud, models, schemas,utils, oauth2
from database import SessionLocal, engine
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from database import get_db
models.Base.metadata.create_all(bind=engine)
import uvicorn

app=FastAPI()


@app.post('/todos',response_model=schemas.Todo,tags=['Todos'])
def create_todo(todo : schemas.TodoCreate,db:Annotated[Session,Depends(get_db)],current_user: Annotated[str,Depends(oauth2.get_current_active_user)]):
    return crud.create_todo(db=db,todo=todo,current_user=current_user)

@app.get('/todos',response_model=list[schemas.Todo],tags=['Todos'])
def get_todos(db:Annotated[Session,Depends(get_db)],current_user:Annotated[str,Depends(oauth2.get_current_active_user)]):
    return crud.get_all(db=db,current_user=current_user)

@app.get('/todos/{todo_id}',response_model=schemas.Todo,tags=['Todos'])
def get_todo(todo_id :int, db:Annotated[Session,Depends(get_db)],current_user:Annotated[str,Depends(oauth2.get_current_active_user)]):
    return crud.get_one(db=db,todo_id=todo_id,current_user=current_user)

@app.delete('/todos/{todo_id}',tags=['Todos'])
def delete_todo(todo_id : int ,db:Annotated[Session,Depends(get_db)],current_user:Annotated[str,Depends(oauth2.get_current_active_user)]):
    return crud.delete_todo(db=db,todo_id=todo_id,current_user=current_user)

@app.put('/todos/{todo_id}',response_model=schemas.Todo,tags=['Todos'])
def update_todo(todo_id:int,post:schemas.TodoCreate,db:Annotated[Session,Depends(get_db)],current_user:Annotated[str,Depends(oauth2.get_current_active_user)]):
    return crud.update_todo(db=db,todo_id=todo_id,post=post,current_user=current_user)

@app.post('/users',response_model=schemas.User,tags=['Users'])
def create_user(user:schemas.UserCreate,db:Annotated[Session,Depends(get_db)]):
    return crud.create_user(db=db,user=user)

@app.get('/users/{user_email}',response_model=schemas.User,tags=['Users'])
def get_user(user_email:EmailStr,db:Annotated[Session,Depends(get_db)],current_user:Annotated[str,Depends(oauth2.get_current_active_user)]):
    return crud.get_user(db=db,user_email=user_email)

@app.post('/login',tags=['login'])
def auth_user(user_credentials: Annotated[OAuth2PasswordRequestForm,Depends()],db:Annotated[Session,Depends(get_db)]):
    db_user=db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if db_user is None:
        raise HTTPException(status_code=403,detail="Invalid Credentials")
    if not utils.verify(user_credentials.password,db_user.password):
        raise HTTPException(status_code=403,detail='Invalid Credentials')
    
    access_token =oauth2.create_access_token(data={'user_email':db_user.email})
    return {'access_token':access_token,'token_type':'bearer'}


    
