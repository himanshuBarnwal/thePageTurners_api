from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from config.db import get_db
from models import Book

autoBook = APIRouter(tags=["autocomplete_book_search"],prefix='/student_search')

@autoBook.get("/book_title", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    
    """
    Provides an auto-complete feature for student searching.
    """
    books = db.query(Book).filter(Book.title.ilike(f"{q}%")).all()
    return [book.title for book in books]

@autoBook.get("/book_author", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    
    """
    Provides an auto-complete feature for student searching.

    :param q: The search query.
    :param db: The database session.
    :return: A list of student names matching the search query.
    """
    books = db.query(Book).filter(Book.author.ilike(f"{q}%")).all()
    return [book.author for book in books]
