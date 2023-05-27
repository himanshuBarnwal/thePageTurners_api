from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from config.db import get_db
from models import Student

autoStudent = APIRouter(tags=["autocomplete_student_search"], prefix='/student_search')


@autoStudent.get("/name", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):

    students = db.query(Student).filter(Student.name.ilike(f"{q}%")).all()
    return list(set([student.name for student in students]))

@autoStudent.get("/course", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    
    students = db.query(Student).filter(Student.course.ilike(f"{q}%")).all()
    return list(set([student.course for student in students]))

@autoStudent.get("/department", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    
    students = db.query(Student).filter(Student.department.ilike(f"{q}%")).all()
    return list(set([student.department for student in students]))


