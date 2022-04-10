import sqlalchemy
from sqlalchemy import Column, Integer, DateTime, CheckConstraint, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, VARCHAR
from dbase.database import Base
from sqlalchemy.dialects import mysql

metadata = sqlalchemy.MetaData()

class Users(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(VARCHAR(30), primary_key=False, nullable=False)
    lastname = Column(VARCHAR(30), primary_key=False, nullable=True)
    email = Column(VARCHAR(40), primary_key=False, nullable=False, unique=True)
    password = Column(VARCHAR(100), primary_key=False, nullable=False)
    role = Column(VARCHAR(30), primary_key=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))
    __table_args__ = (CheckConstraint(role.in_(['Student', 'Admin', 'Tutor'])),)


contact_int = mysql.INTEGER

class Student(Base):
    __tablename__ = 'Student'
    stu_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    dob = Column(DateTime, nullable=False)
    course_name = Column(VARCHAR(20), nullable=False)
    address = Column(VARCHAR(100), nullable=False)
    contact_no = Column(contact_int(10))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))
    __table_args__ = (CheckConstraint(course_name.in_(['Python', 'Java'])),)


class Admin(Base):
    __tablename__ = 'Admin'
    admin_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    dob = Column(DateTime, nullable=False)
    address = Column(VARCHAR(100), nullable=False)
    contact_no = Column(contact_int(10))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))

class Tutor(Base):
    __tablename__ = 'Tutor'
    tutor_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    tutor_of = Column(VARCHAR(20), nullable=False, unique=True)
    dob = Column(DateTime, nullable=False)
    address = Column(VARCHAR(100), nullable=False)
    contact_no = Column(contact_int(10))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))
    __table_args__ = (CheckConstraint(tutor_of.in_(['Python', 'Java'])),)


class RecRequest(Base):
    __tablename__ = 'RecReq'
    req_id = Column(Integer, primary_key=True, nullable=False)
    stu_email = Column(VARCHAR(40), ForeignKey("User.email"), primary_key=False, nullable=False)
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
    __tablename__ = 'DCSReq'
    req_id = Column(Integer, primary_key=True, nullable=False)
    stu_email = Column(VARCHAR(40), ForeignKey("User.email"), primary_key=False, nullable=False)
    subject = Column(VARCHAR(20), nullable=False)
    topic = Column(VARCHAR(70), nullable=False)
    req_reason = Column(VARCHAR(100), nullable=False)
    req_status = Column (VARCHAR(30), server_default="Pending", nullable=False)
    comment = Column(VARCHAR(100), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now() ON UPDATE now()'))
    __table_args__ = (CheckConstraint(req_status.in_(['Pending', 'Approved', 'Rejected', 'Forwarded'])),
                      CheckConstraint(subject.in_(['Python', 'Java'])))

class BlackListedTokens(Base):
    __tablename__ = 'Blacklists'
    token_id = Column(Integer, primary_key=True, nullable=False)
    token = Column(VARCHAR(250), unique=True)
    email = Column(VARCHAR(40))



