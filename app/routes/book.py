from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
from config.db import get_db,Base
from models import Book, BookRequest
from schemas import book as schema
from typing import Optional, List
import pandas as pd
from respository.my_token import is_admin_authenticated
from respository import oauth2
from schemas import student

book = APIRouter(tags=["book"],prefix='/book')
# , HTTPException
@book.post("/addBook",)
async def add_book(books:List[schema.BookCreate],db:Session = Depends(get_db), is_auth=Depends(is_admin_authenticated)):
    
    try:
        if is_auth:
            book_list=[]
            for book in books:
                db_book = Book(**book.dict())
                db.add(db_book)
                book_list.append(db_book)
            db.commit()
            db.refresh(db_book)
                
            return book_list
        else:
            return {'msg':'Please login first'}
        # db.refresh(db_book)
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))


@book.put("/updateBook")
async def update_book(books:List[schema.BookUpdate],db:Session = Depends(get_db),is_auth=Depends(is_admin_authenticated)):
    try:
        if is_auth:
            for book in books:
                isbn = book.isbn
                update_data = book.dict(exclude_unset=True)
                db.execute(update(Book).where(Book.isbn == isbn).values(**update_data))
            db.commit()
            return {"message": "Books updated successfully"}
        else:
            return {'msg':'Please login first'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# endpoint to delete a book
@book.delete("/deleteBook")
async def delete_book(isbns:List[str],db:Session = Depends(get_db)):
    try:
        if is_auth:
            for isbn in isbns:
                db_book = db.query(Book).filter(Book.isbn == isbn).first()
                if not db_book:
                    raise HTTPException(status_code=404, detail=f"Book {isbn} not found")
                db.delete(db_book)
            db.commit()
            return {"msg":"Books deleted Sucessfully"}
        else:
            return {'msg':'Please login first'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@book.get("/getAllBook", response_model=List[schema.Book])
async def get_all_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

@book.post("/add_book_csv")
async def addBook(path:str, db: Session = Depends(get_db)):
    print("pathfhff",path)
    try:
        df = pd.read_csv(path)
        # lst = []
        # for i in df:
        #     lst.append(i)+
        print(df.head())
        bookList=[]
        for row in df.index:
            db_query = db.query(Book).filter(df['ISBN'][row]==Book.isbn).first()
            if not db_query:
                title = df['Title'][row], 
                author = df['Author'][row],
                genre = df['Genre'][row],
                year_of_publication= df['Year of Publication'][row],
                isbn= df['ISBN'][row]
                db_book = Book(
                    title = title[0], 
                    author = author[0],
                    genre = genre[0],
                    year_of_publication= year_of_publication,
                    isbn= isbn
                ) 
                db.add(db_book)
                bookList.append(db_book)
        db.commit()
        db.refresh(db_book)
        return bookList
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))
    

# , response_model=BookRecommendationResponse
@book.get('/recommend_book')
def recommend_books(genre: str, db: Session = Depends(get_db), current_user: student.Student = Depends(oauth2.get_current_user)):
    # Check if the student ID and ISBN are valid
    '''Genre = [ ]'''
    try:
        db_book = db.query(Book).filter((Book.genre==genre)&(Book.available==True)).all()
        s_id = current_user.id
        lst = []
        cnt=0
        print(len(db_book))
        for book in db_book:
            check = db.query(BookRequest).filter((BookRequest.isbn==book.isbn)&(BookRequest.student_id==s_id)).first()
            if not check:
                lst.append(book)
                cnt+=1
                if cnt==5:
                    break
        return lst
    except:
        raise HTTPException(status_code=404, detail="There is no recommended book of this genre")


    return recommended_books
