from pydantic import BaseModel, EmailStr


class Registration(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    role: str

class RegiOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    role: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserDetails(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    class Config:
        orm_mode = True

