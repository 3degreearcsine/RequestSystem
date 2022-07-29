from passlib.context import CryptContext
from sqlalchemy.orm import Query
from app.dbase import models, database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

async def verfiy(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def check_if_blacklisted(token: str):
    b_l_t = Query([models.BlackListedTokens]).filter(models.BlackListedTokens.token == token)
    b_l_t_result = b_l_t.with_session(database.session).first()
    return b_l_t_result

def check_if_admin_exist(role: str):
    chk_admin_exist = Query([models.Users]).filter(models.Users.role == role)
    chk_admin_exist_result = chk_admin_exist.with_session(database.session).first()
    return chk_admin_exist_result

def check_course(id: int, subject: str):
    chk_course = Query([models.Student]).filter(models.Student.user_id == id).filter(models.Student.course_name
                                                                                     == subject)
    chk_course_result = chk_course.with_session(database.session).first()
    return chk_course_result

def check_tutor_course(id: int):
    chk_tut_course = Query([models.Tutor]).filter(models.Tutor.user_id == id)
    chk_tut_course_result = chk_tut_course.with_session(database.session).first()
    return chk_tut_course_result