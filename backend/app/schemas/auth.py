from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole
class RegisterIn(BaseModel):
    name: str = Field(min_length=2,max_length=120)
    email: EmailStr
    password: str = Field(min_length=8,max_length=128)
class LoginIn(BaseModel):
    email: EmailStr
    password: str
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
class UserOut(BaseModel):
    id:int; name:str; email:EmailStr; role:str

class AdminUserOut(BaseModel):
    id:int; name:str; email:EmailStr; role:UserRole; is_active:bool; official_title:str|None=None

class UserRoleUpdate(BaseModel):
    role:UserRole
    official_title:str|None=Field(default=None,min_length=2,max_length=100)
    party:str|None=Field(default=None,max_length=120)
