import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from app.dbase.config import settings

SQLALCHEMY_DATABASE_URL = f'mysql+mysqlconnector://{settings.database_username}:{settings.database_password}' \
                          f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
database = databases.Database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)
Base = declarative_base()
Base.query = session.query_property()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()






