from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from tools import hash
import database, models, schemas
from tools.token import create_access_token

getdb = database.getdb

router = APIRouter(tags=["user"])

@router.get("/user", response_model=list[schemas.BaseUser])
def list_user(db:Session=Depends(getdb)):

    users = db.query(models.User).all()

    return users

@router.post("/user", response_model=schemas.BaseUser)
def create_user(req:schemas.CreateUser, db:Session=Depends(getdb)):
    new_user = models.User(username=req.username, password=hash.password_hash(req.password), email=req.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login_user(req:schemas.Login, db:Session=Depends(getdb)):
    user = db.query(models.User).filter(models.User.username == req.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if not hash.verify_password(req.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "user":{"id":user.id, "username":user.username, "email":user.email}}