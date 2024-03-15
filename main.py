from fastapi import FastAPI 
import models as models
#from starlette.staticfiles import StaticFiles
from database import engine

from routers import auth , checklist,admin

app =FastAPI()

models.Base.metadata.create_all(bind =engine)

#app.mount('/static',StaticFiles(directory='static'),name='static')

app.include_router(auth.router)
app.include_router(checklist.router)
app.include_router(admin.router)

