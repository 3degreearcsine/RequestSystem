from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
from fastapi import Form
from datetime import datetime, date


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
    firstname: constr(to_lower=True)
    lastname: constr(to_lower=True)
    email: EmailStr
    password: str
    role: constr(to_lower=True)


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


@form_body
class StudentInfo(BaseModel):
    dob: date
    course_name: constr(to_lower=True)
    address: constr(to_lower=True)
    contact_no: int


class StudentDetails(BaseModel):
    stu_id: int
    user_id: int
    dob: date
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


@form_body
class AdminInfo(BaseModel):
    dob: date
    address: constr(to_lower=True)
    contact_no: int


class AdminDetails(BaseModel):
    admin_id: int
    user_id: int
    dob: date
    address: str
    contact_no: int

    class Config:
        orm_mode = True


class AdminAllDetails(BaseModel):
    Users: UserDetails
    Admin: AdminDetails

    class Config:
        orm_mode = True


@form_body
class TutorInfo(BaseModel):
    tutor_of: constr(to_lower=True)
    dob: date
    address: constr(to_lower=True)
    contact_no: int


class TutorDetails(BaseModel):
    tutor_id: int
    user_id: int
    tutor_of: str
    dob: date
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
    lec_date: date
    subject: constr(to_lower=True)
    req_reason: constr(to_lower=True)


class RecReqOut(BaseModel):
    req_id: int
    stu_email: str
    lec_date: date
    subject: str
    req_reason: str
    req_status: str
    comment: Optional[str]
    created_at: date
    last_updated: date

    class Config:
        orm_mode = True


class ReqDelete(BaseModel):
    req_id: int


class ReqAction(BaseModel):
    req_id: int
    req_status: constr(to_lower=True)
    comment: Optional[constr(to_lower=True)]


class DCSReq(BaseModel):
    subject: constr(to_lower=True)
    topic: constr(to_lower=True)
    req_reason: constr(to_lower=True)


class DCSReqOut(BaseModel):
    req_id: int
    stu_email: str
    subject: str
    topic: str
    req_reason: str
    req_status: str
    comment: Optional[str]
    created_at: date
    last_updated: date

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
