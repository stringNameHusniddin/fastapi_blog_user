from fastapi import FastAPI 
from routers import user
import database, models 

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(router=user.router)