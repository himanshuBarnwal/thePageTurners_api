
from sqlalchemy import Column, Integer, String, Date, LargeBinary, ForeignKey, DateTime, Boolean

from config.db import Base

#students
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    roll_number = Column(String(10), unique=True)
    course = Column(String(50))
    department = Column(String(50))
    year_of_admission = Column(Integer)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(64))
    
    # def to_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
#admin
class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    name = Column(String(50))
    email = Column(String(50),unique=True,index=True)
    password = Column(String(64))
    role = Column(String(20))
#books table
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String(100), index=True)
    author = Column(String(100), index=True)
    genre = Column(String(50))
    year_of_publication = Column(Integer)
    isbn = Column(String(17), unique=True, index=True)
    available = Column(Boolean, default = True)
    
#Connection table
class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("students.id"), index=True)
    receiver_id = Column(Integer, ForeignKey("students.id"), index=True)
    status = Column(String(10))
    created_at = Column(DateTime)
    


# #Borrowed books
# class BorrowedBook(Base):
#     __tablename__ = "borrowed_books"

#     id = Column(Integer, primary_key=True, index=True)
#     student_id = Column(Integer, ForeignKey("students.id"), index=True)
#     isbn = Column(Integer, ForeignKey("books.isbn"), index=True)
#     borrowed_date = Column(Date)
#     return_date = Column(Date)
    
#Borrowed Request
#Pending, Accept, Decline
class BookRequest(Base):
    __tablename__ = "book_request"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True)
    isbn = Column(String(17), ForeignKey("books.isbn"), index=True)
    request_date = Column(DateTime)
    status = Column(String(10))
    reviewed_at = Column(DateTime)
    
#Book Search
# class BookSearch(Base):
#     __tablename__ = "book_searches"

#     id = Column(Integer, primary_key=True, index=True)
#     student_id = Column(Integer, ForeignKey("students.id"), index=True)
#     search_query = Column(String(100), index=True)
    
#students search
# class StudentSearch(Base):
#     __tablename__ = "student_searches"

#     id = Column(Integer, primary_key=True, index=True)
#     student_id = Column(Integer, ForeignKey("students.id"), index=True)
#     search_query = Column(String(100), index=True)
    
