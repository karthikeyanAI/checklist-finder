from fastapi import APIRouter ,Depends ,HTTPException ,Path ,Request
from models import  checklist
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from pydantic import BaseModel ,Field

from AI.prompts import generate
from .auth import get_current_user


from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router =APIRouter(
       prefix="/checklist",
    tags=["checklist"],
    responses={404:{"description":"Not found"}}
)


templates =Jinja2Templates(
    directory="templates"
)
def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency =Annotated[Session , Depends(get_db)]
user_dependency =Annotated[dict,Depends(get_current_user)]


class Userresponse_model(BaseModel):
    username:str
    errorcode:str
    checklist:str
    owner_id:int




@router.post("/response",)
async def response(
    query:str,
    current_user:user_dependency,
    db:db_dependency

    ):

    response=generate(query)

    create_user_history=checklist(
        
    username=current_user.get('username'),
    errorcode=str(query),
    checklist =str(response),
    owner_id =current_user.get('id')
    )
    db.add(create_user_history)
    db.commit()


    return {'response':response}


@router.get("/",status_code=status.HTTP_200_OK)
async def  read_all(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    return db.query(checklist).filter(checklist.owner_id==user.get("id")).all()