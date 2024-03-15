
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL ='postgresql://postgres:test12@localhost/checklist'


engine =create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal =sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()