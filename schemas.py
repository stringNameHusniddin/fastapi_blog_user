from pydantic import BaseModel

class BaseUser(BaseModel):
    username : str
    email : str

class CreateUser(BaseUser):
    password : str

class Login(BaseModel):
    username : str
    password : str

class TokenData(BaseModel):
    username : str