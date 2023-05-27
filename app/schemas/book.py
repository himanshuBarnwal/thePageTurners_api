from pydantic import BaseModel
from typing import Optional
class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_of_publication: int
    isbn: str


class BookUpdate(BaseModel):
    isbn: str
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_of_publication: Optional[int] = None
    
class BookDelete(BaseModel):
    isbn:str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available:bool

    class Config:
        orm_mode = True


class BookRecommendationBase(BaseModel):
    student_id: int

class BookRecommendationCreate(BookRecommendationBase):
    pass

class BookRecommendation(BookRecommendationBase):
    id: int

    class Config:
        orm_mode = True
