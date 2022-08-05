from passlib.context import CryptContext
from sqlalchemy.orm import Query
from app.dbase import models, database
from jose import JWTError, jwt
from app.dbase.config import settings
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verfiy(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def check_if_blacklisted(token: str):
    b_l_t = Query([models.BlackListedTokens]).filter(models.BlackListedTokens.token == token)
    b_l_t_result = b_l_t.with_session(database.session).first()
    return b_l_t_result


def check_if_admin_exist(role: str):
    chk_admin_exist = Query([models.Users]).filter(models.Users.role == role)
    chk_admin_exist_result = chk_admin_exist.with_session(database.session).first()
    return chk_admin_exist_result

def check_if_profile_complete(user_id: int, role: str):
    if role == 'student':
        chk_stu_profile = Query([models.Student]).filter(models.Student.user_id == user_id)
        chk_stu_profile_result = chk_stu_profile.with_session(database.session).first()
        return chk_stu_profile_result
    elif role == 'tutor':
        chk_tut_profile = Query([models.Tutor]).filter(models.Tutor.user_id == user_id)
        chk_tut_profile_result = chk_tut_profile.with_session(database.session).first()
        return chk_tut_profile_result
    elif role == 'admin':
        chk_admin_profile = Query([models.Admin]).filter(models.Admin.user_id == user_id)
        chk_admin_profile_result = chk_admin_profile.with_session(database.session).first()
        return chk_admin_profile_result


def check_if_token_expired(token: str):
    try:
        jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    except jwt.ExpiredSignatureError:
        return True


def check_if_email_exists(email: str):
    chk_email_exists =  Query([models.Users]).filter(models.Users.email == email)
    chk_email_exists_result = chk_email_exists.with_session(database.session).first()
    return chk_email_exists_result


def check_course(id: int, subject: str):
    chk_course = Query([models.Student]).filter(models.Student.user_id == id).filter(models.Student.course_name
                                                                                     == subject)
    chk_course_result = chk_course.with_session(database.session).first()
    return chk_course_result


def check_tutor_course(id: int):
    chk_tut_course = Query([models.Tutor]).filter(models.Tutor.user_id == id)
    chk_tut_course_result = chk_tut_course.with_session(database.session).first()
    return chk_tut_course_result