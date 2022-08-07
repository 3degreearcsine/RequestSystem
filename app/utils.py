from passlib.context import CryptContext
from sqlalchemy.orm import Query
from app.dbase import models, database
from jose import jwt
from app.dbase.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verfiy(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def check_if_blacklisted(token: str):
    b_l_t_result = Query([models.BlackListedTokens]).filter(models.BlackListedTokens.token == token).with_session(database.session).first()
    return b_l_t_result


def check_if_admin_exist(role: str):
    chk_admin_exist_result = Query([models.Users]).filter(models.Users.role == role).with_session(database.session).first()
    return chk_admin_exist_result


def check_if_profile_complete(user_id: int, role: str):
    if role == 'student':
        chk_stu_profile_result = Query([models.Student]).filter(models.Student.user_id ==
                                                                user_id).with_session(database.session).first()
        return chk_stu_profile_result
    elif role == 'tutor':
        chk_tut_profile_result = Query([models.Tutor]).filter(models.Tutor.user_id ==
                                                              user_id).with_session(database.session).first()
        return chk_tut_profile_result
    elif role == 'admin':
        chk_admin_profile_result = Query([models.Admin]).filter(models.Admin.user_id ==
                                                                user_id).with_session(database.session).first()
        return chk_admin_profile_result


def check_if_token_expired(token: str):
    try:
        jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    except jwt.ExpiredSignatureError:
        return True


def check_if_email_exists(email: str):
    chk_email_exists_result = Query([models.Users]).filter(models.Users.email ==
                                                           email).with_session(database.session).first()
    return chk_email_exists_result


def check_course(id: int, subject: str):
    chk_course_result = Query([models.Student]).filter(models.Student.user_id ==
                                                       id).filter(models.Student.course_name == subject).with_session(database.session).first()
    return chk_course_result


def check_tutor_course(id: int):
    chk_tut_course_result = Query([models.Tutor]).filter(models.Tutor.user_id ==
                                                         id).with_session(database.session).first()
    return chk_tut_course_result

def check_if_tutor_exists(tutor_of: str):
    chk_tut_already_exists_result = Query([models.Tutor]).filter(models.Tutor.tutor_of ==
                                                                 tutor_of).with_session(database.session).first()
    return chk_tut_already_exists_result
