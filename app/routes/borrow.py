from fastapi import APIRouter, Depends, status, HTTPException 
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.db import get_db
from respository.oauth2 import get_current_user
from models import BookRequest, Book
from schemas import bookReq, student
from datetime import datetime

borrow = APIRouter(tags=["Book Borrow"], prefix='/book_issue')

@borrow.post("/request")
async def book_issue_request(request: bookReq.IssueRequest, db: Session = Depends(get_db), current_user: student.Student = Depends(get_current_user)):
    borrower_id = current_user.id
    book_isbn = request.isbn
    
    # find the book in the library based on ISBN
    db_book = db.query(Book).filter(Book.isbn == book_isbn).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found in library")
    

    request_record = BookRequest(student_id = borrower_id,
                                 isbn = request.isbn,
                                 request_date = datetime.now(), 
                                 status="Pending")
    db.add(request_record)
    db.commit()
    db.refresh(request_record)
    return request_record

#request.status = accepted to issue to book and issue.status = rejected to decline the request. 
@borrow.post("/action",response_class = JSONResponse)
async def book_issue_action(request:bookReq.IssueUpdate, db: Session = Depends(get_db), current_admin: student.Student = Depends(get_current_user)):
    
    db_book_req = db.query(BookRequest).filter((BookRequest.isbn == request.isbn) & (BookRequest.status=="Pending")).first()
    if not db_book_req:
        raise HTTPException(status_code=404, detail="Book not found in request table")
    else:
        db_book_req.status = request.status
        db_book_req.reviewed_at = datetime.now()
        db.add(db_book_req)
        db.commit()
        db.refresh(db_book_req)
        x = db_book_req
        
        if request.status == "accepted":
            db_book = db.query(Book).filter(Book.isbn==request.isbn).first()
            db_book.available = 0
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            
        return x

