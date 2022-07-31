import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import Form


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form())
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

@form_body
class Registration(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    role: str


class RegistrationOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    role: str
    email: EmailStr

    class Config:
        orm_mode = True


@form_body
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserDetails(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr

    class Config:
        orm_mode = True


class StudentInfo(BaseModel):
    dob: datetime.date
    course_name: str
    address: str
    contact_no: int


class StudentDetails(BaseModel):
    stu_id: int
    user_id: int
    dob: datetime.date
    course_name: str
    address: str
    contact_no: int

    class Config:
        orm_mode = True


class StudentAllDetails(BaseModel):
    Users: UserDetails
    Student: StudentDetails

    class Config:
        orm_mode = True


class AdminInfo(BaseModel):
    dob: datetime.date
    address: str
    contact_no: int


class AdminDetails(BaseModel):
    admin_id: int
    user_id: int
    dob: datetime.date
    address: str
    contact_no: int

    class Config:
        orm_mode = True


class AdminAllDetails(BaseModel):
    Users: UserDetails
    Admin: AdminDetails

    class Config:
        orm_mode = True


class TutorInfo(BaseModel):
    tutor_of: str
    dob: datetime.date
    address: str
    contact_no: int


class TutorDetails(BaseModel):
    tutor_id: int
    user_id: int
    tutor_of: str
    dob: datetime.date
    address: str
    contact_no: int

    class Config:
        orm_mode = True


class TutorAllDetails(BaseModel):
    Users: UserDetails
    Tutor: TutorDetails

    class Config:
        orm_mode = True


class AllStudents(BaseModel):
    Users: RegistrationOut
    Student: StudentDetails

    class Config:
        orm_mode = True


class AllTutors(BaseModel):
    Users: RegistrationOut
    Tutor: TutorDetails

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
    comment: Optional[str]
    created_at: datetime.datetime
    last_updated: datetime.datetime

    class Config:
        orm_mode = True


class ReqDelete(BaseModel):
    req_id: int


class ReqAction(BaseModel):
    req_id: int
    req_status: str
    comment: Optional[str]


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
    comment: Optional[str]
    created_at: datetime.datetime
    last_updated: datetime.datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    token: Optional[str] = None
