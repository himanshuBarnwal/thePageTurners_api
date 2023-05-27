from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db,Base
from models import Student
from schemas import student as schema
from typing import Optional
from respository.hashing import Hash
# import respository.oauth2, respository.my_token
from fastapi.security import OAuth2PasswordRequestForm
from respository import oauth2,my_token



student = APIRouter(tags=['Student'] )


@student.post("/signUp",response_model=schema.Student)
async def create_student(request: schema.StudentBase, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.email == request.email).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_student = db.query(Student).filter(Student.roll_number == request.roll_number).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Roll number already registered")

    db_student = Student(
        name=request.name, 
        roll_number=request.roll_number,
        course=request.course, 
        department=request.department,
        year_of_admission=request.year_of_admission, 
        email=request.email,
        password=Hash.bcrypt(request.password)
    )    
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student
# student_id: int,
# , response_model=schema.Student


@student.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Student).filter(
        Student.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = my_token.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@student.get("/getStudentDetails")
def get_student( db: Session = Depends(get_db), current_user: schema.Student = Depends(oauth2.get_current_user)):
    db_student = db.query(Student).filter(Student.id == current_user.id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@student.get("/friend_recommended")
async def recommended_friend(db: Session = Depends(get_db), current_user: schema.Student = Depends(oauth2.get_current_user)):
    try:
        s_id = current_user.id
        
        db_student = db.query(Student).filter(Student.id==s_id).first()
        department = db_student.department
        course = db_student.course
        
        db_common = db.query(Student).filter((Student.department==department)|(Student.course==course)).limit(5).all()
        # books = db.query(Book).offset(skip).limit(limit).all()
        return db_common
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))
    

