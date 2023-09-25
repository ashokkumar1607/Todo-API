from jose import JWTError, jwt
from datetime import datetime, timedelta
import schemas, models
from fastapi import Depends, status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from typing import Annotated


oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY='09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data:dict):
    to_enocde=data.copy()
    expire =datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enocde.update({'exp':expire})

    encoded_jwt = jwt.encode(to_enocde,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db : Annotated[Session,Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("user_email")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(token_data.email == models.User.email).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

