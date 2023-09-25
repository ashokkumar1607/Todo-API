from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text, DateTime
import sqlalchemy
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Todo(Base):
    __tablename__ = 'todos'

    id=Column(Integer,primary_key=True,index=True)
    task=Column(Integer)
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=sqlalchemy.sql.func.now())
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)


class User(Base):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=sqlalchemy.sql.func.now())