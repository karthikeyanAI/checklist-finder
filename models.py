from database import Base
from sqlalchemy import Column ,Integer,String,Boolean,ForeignKey



class User(Base):
    __tablename__ ='users'

    id = Column(Integer, primary_key=True ,index=True)
    email  =Column(String,unique=True)
    username =Column(String,unique=True)
    hashed_password=Column(String)
    role =Column(String)
    

class checklist(Base):
    __tablename__='userresponse'

    id=Column(Integer ,primary_key=True,index=True)
    username=Column(String,ForeignKey("users.username"))
    errorcode=Column(String)
    checklist =Column(Integer)
    owner_id =Column(Integer,ForeignKey("users.id"))

