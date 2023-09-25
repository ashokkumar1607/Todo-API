from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr


class TodoBase(BaseModel):
    task : str 

class TodoCreate(TodoBase):
    pass 

class Todo(TodoBase):
    id : int
    created_at : datetime
    user_id : int

    class config:
        orm_mode=True

class UserBase(BaseModel):
    email : EmailStr

class UserCreate(UserBase):
    password : str

class User(UserBase):
    id : int
    created_at : datetime

    class config:
        orm_mode=True


class Token(BaseModel):
    access_token: str
    token_type : str 

class TokenData(BaseModel):
    email:str