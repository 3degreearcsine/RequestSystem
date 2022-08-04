import sqlalchemy
from sqlalchemy import Column, Integer, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, VARCHAR
from app.dbase.database import Base
from sqlalchemy.dialects import mysql

metadata = sqlalchemy.MetaData()


class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(VARCHAR(30), primary_key=False, nullable=False)
    lastname = Column(VARCHAR(30), primary_key=False, nullable=True)
    email = Column(VARCHAR(40), primary_key=False, nullable=False, unique=True)
    password = Column(VARCHAR(100), primary_key=False, nullable=False)
    role = Column(VARCHAR(30), primary_key=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))
    __table_args__ = (CheckConstraint(role.in_(['Student', 'Admin', 'Tutor'])),)


contact_int = mysql.BIGINT

class Student(Base):
    __tablename__ = 'student'
    stu_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    dob = Column(DateTime, nullable=False)
    course_name = Column(VARCHAR(20), nullable=False)
    address = Column(VARCHAR(100), nullable=False)
    contact_no = Column(contact_int(10), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))
    __table_args__ = (CheckConstraint(course_name.in_(['Python', 'Java'])), CheckConstraint('contact_no>=1000000000'),
                      CheckConstraint('contact_no<=9999999999'))


class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    dob = Column(DateTime, nullable=False)
    address = Column(VARCHAR(100), nullable=False)
    contact_no = Column(contact_int(10), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))
    __table_args__ = (CheckConstraint('contact_no>=1000000000'), CheckConstraint('contact_no<=9999999999'))


class Tutor(Base):
    __tablename__ = 'tutor'
    tutor_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    tutor_of = Column(VARCHAR(20), nullable=False, unique=True)
    dob = Column(DateTime, nullable=False)
    address = Column(VARCHAR(100), nullable=False)
    contact_no = Column(contact_int(10), unique=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))
    __table_args__ = (CheckConstraint(tutor_of.in_(['python', 'java'])), CheckConstraint('contact_no>=1000000000'),
                      CheckConstraint('contact_no<=9999999999'))


class RecRequest(Base):
    __tablename__ = 'recreq'
    req_id = Column(Integer, primary_key=True, nullable=False)
    stu_email = Column(VARCHAR(40), ForeignKey("user.email"), primary_key=False, nullable=False)
    lec_date = Column(DateTime, nullable=False)
    subject = Column(VARCHAR(20), nullable=False)
    req_reason = Column(VARCHAR(100), nullable=False)
    req_status = Column(VARCHAR(30), server_default="Pending", nullable=False)
    comment = Column(VARCHAR(100), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))
    __table_args__ = (CheckConstraint(req_status.in_(['Pending', 'Approved', 'Rejected'])),
                      CheckConstraint(subject.in_(['Python', 'Java'])))


class SessionRequest(Base):
    __tablename__ = 'dcsreq'
    req_id = Column(Integer, primary_key=True, nullable=False)
    stu_email = Column(VARCHAR(40), ForeignKey("user.email"), primary_key=False, nullable=False)
    subject = Column(VARCHAR(20), nullable=False)
    topic = Column(VARCHAR(70), nullable=False)
    req_reason = Column(VARCHAR(100), nullable=False)
    req_status = Column(VARCHAR(30), server_default="Pending", nullable=False)
    comment = Column(VARCHAR(100), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))
    __table_args__ = (CheckConstraint(req_status.in_(['Pending', 'Accepted', 'Rejected', 'Forwarded'])),
                      CheckConstraint(subject.in_(['Python', 'Java'])))


class BlackListedTokens(Base):
    __tablename__ = 'blacklists'
    token_id = Column(Integer, primary_key=True, nullable=False)
    token = Column(VARCHAR(250), unique=True)
    email = Column(VARCHAR(40))
