from fastapi import APIRouter ,Depends ,HTTPException ,Path
from models import checklist
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel ,Field

from routers.checklist import Userresponse_model
from .auth import get_current_user

router =APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency =Annotated[Session , Depends(get_db)]
user_dependency =Annotated[dict,Depends(get_current_user)]




@router.get("/admin",status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency,db:db_dependency):
    if user is None or user.get('role')!='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(checklist).all()



