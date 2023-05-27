from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from config.db import get_db
from models import Student

autoStudent = APIRouter(tags=["autocomplete_student_search"], prefix='/book_search')


@autoStudent.get("/sname", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):

    """
    Provides an auto-complete feature for student searching.
    :param q: The search query.
    :return: A list of student names matching the search query.
    """
    students = db.query(Student).filter(Student.name.ilike(f"{q}%")).all()
    return [student.name for student in students]

@autoStudent.get("/scourse", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    
    """
    Provides an auto-complete feature for student searching.
    """
    students = db.query(Student).filter(Student.course.ilike(f"{q}%")).all()
    return [student.course for student in students]

@autoStudent.get("/sdepartment", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    
    """
    Provides an auto-complete feature for student searching..
    """
    students = db.query(Student).filter(Student.department.ilike(f"{q}%")).all()
    return [student.department for student in students]


