from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from config.db import get_db
from models import Book

autoBook = APIRouter(tags=["autocomplete_book_search"],prefix='/book_search')

@autoBook.get("/title", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):

    books = db.query(Book).filter(Book.title.ilike(f"{q}%")).all()
    return [book.title for book in books]

@autoBook.get("/author", response_model=List[str])
def autocomplete(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    
    books = db.query(Book).filter(Book.author.ilike(f"{q}%")).all()
    return [book.author for book in books]
