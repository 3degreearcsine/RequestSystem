import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


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


class RecReq(BaseModel):
    lec_date: datetime.date
    subject: str
    req_reason: str

class RecReqOut(BaseModel):
    req_id: int
    stu_email: str
    lec_date: datetime.date
    subject: str
    req_reason: str
    req_status: str
    created_at: datetime.datetime
    last_updated: datetime.datetime

    class Config:
        orm_mode = True

class DCSReq(BaseModel):
    subject: str
    topic: str
    req_reason: str

class DCSReqOut(BaseModel):
    req_id: int
    stu_email: str
    subject: str
    topic: str
    req_reason: str
    req_status: str
    created_at: datetime.datetime
    last_updated: datetime.datetime

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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None

class log_out(BaseModel):
    token: Optional[str] = None
    class Config:
        orm_mode = True
