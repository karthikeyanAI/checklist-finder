from fastapi import FastAPI ,APIRouter ,Depends ,HTTPException
from pydantic import BaseModel
from models import User
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm ,OAuth2PasswordBearer
from datetime import timedelta,datetime

from jose import jwt ,JWTError




router =APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY ='jkbkasbcsbcjbciusbcjdkjzubiudbujbsjcbias'
ALGORITHAM ='HS256'


bcrypt_context =CryptContext(schemes=['bcrypt'], deprecated ='auto')
oauth2_bearer =OAuth2PasswordBearer(tokenUrl='auth/token')


class Usermodel(BaseModel):
    email :str 
    username :str
    hashed_password:str
    role :str

class Token(BaseModel):
    access_token:str
    token_type:str

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency =Annotated[Session , Depends(get_db)]



def authenticate_user(username:str ,password: str ,db:db_dependency):
    user =db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def get_user(username:str,db:db_dependency):
    user =db.query(User).filter(User.username == username).first()
    if not user:
        return False
    return user


def create_access_token(username:str ,user_id:int ,role:str,expires_delta :timedelta):
    encode ={'sub':username,'id':user_id,'role':role}
    expires =datetime.now()+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHAM)

async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)],db:db_dependency):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHAM])
        username:str =payload.get('sub')
        user_id:int =payload.get('id')
        user_role:str =payload.get('role')
        # user = get_user(username,db)
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
        return {'username':username,"id":user_id,'role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')






@router.post("/user/register",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:Usermodel):
    create_user_model =User(
        email =create_user_request.email,
        username=create_user_request.username,
        role =create_user_request.role,
        hashed_password =bcrypt_context.hash(create_user_request.hashed_password)
    
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token",response_model=Token)
async def login_for_access_token(form_data : Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user =authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
    
    token =create_access_token(user.username ,user.id,user.role,timedelta(minutes=20))
    
    return {'access_token':token ,'token_type':'bearer'}
