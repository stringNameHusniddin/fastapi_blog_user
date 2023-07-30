from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from tools import oauth2
import database, models, schemas, uuid 

router = APIRouter(tags=["blog"])

getdb =  database.getdb

@router.get("/blog")
def list_blogs(db:Session=Depends(getdb), current_user:schemas.BaseUser=Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()

    return blogs 

@router.get("/images/{filename}")
def get_image(filename:str):
    return FileResponse(f"images/{filename}")

@router.post("/blog")
async def create_blog(name:str=Form(...), body:str=Form(...), file:UploadFile=File(...), owner_id:int=Form(...), db:Session=Depends(getdb)):
    content = await file.read()

    filename = f"images/{uuid.uuid4()}.jpg"

    with open(filename, "wb") as f:
        f.write(content)

    new_blog = models.Blog(name = name, body = body, owner_id=owner_id, url=f"http://127.0.0.1:8000/{filename}")

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

