from sqlalchemy import Boolean, Column, Integer, String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime

Base=declarative_base()

class Student(Base):
    __tablename__="student"
    id=Column(Integer,primary_key=True)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)

class Book(Base):
    __tablename__="books"
    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String)
    author=Column(String)
    category=Column(String)
    available=Column(Boolean, default=True)    

class Borrow(Base):
    __tablename__="borrow"
    id=Column(Integer,primary_key=True,nullable=False)
    book_id=Column(Integer,ForeignKey("books.id"))
    stud_id=Column(Integer,ForeignKey("student.id"))
    borrow_date = Column(DateTime)
    return_date = Column(DateTime, nullable=True)
    fine = Column(Integer, default=0)
    paid = Column(Boolean, default=False)

