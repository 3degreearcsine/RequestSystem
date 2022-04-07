from passlib.context import CryptContext
from sqlalchemy.orm import Query
from dbase import models, database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

async def verfiy(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def check_if_blacklisted(token: str):
    b_l_t = Query([models.BlackListedTokens]).filter(models.BlackListedTokens.token == token)

    b_l_t_result = b_l_t.with_session(database.session).first()
    return b_l_t_result