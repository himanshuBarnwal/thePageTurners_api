from typing import Optional
from pydantic import BaseModel
from fastapi import UploadFile


class StudentBase(BaseModel):
    name: str
    roll_number: str
    course: str
    department: str
    year_of_admission: int
    email: str
    password: str

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    # profile_picture: Optional[UploadFile] = None

    class Config:
        orm_mode = True
        
class LoginRequestForm(BaseModel):
    username: str
    password: str