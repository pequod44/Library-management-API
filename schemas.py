from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime
from typing import Optional, List

class AuthorBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    birth_date: Optional[date] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    available_copies: int = Field(default=1, ge=0)
    author_id: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BorrowBase(BaseModel):
    book_id: int
    reader_name: str = Field(..., min_length=2, max_length=100)

class BorrowCreate(BorrowBase):
    pass

class BorrowResponse(BorrowBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)