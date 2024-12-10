from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from db import SessionLocal, engine
import models
import schemas
from CRUD import AuthorRepository, BookRepository, BorrowRepository

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Library")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинты для авторов
@app.post("/authors", response_model=schemas.AuthorResponse)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return AuthorRepository.create(db, author)

@app.get("/authors", response_model=List[schemas.AuthorResponse])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return AuthorRepository.get_all(db, skip, limit)

@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def read_author(author_id: int, db: Session = Depends(get_db)):
    return AuthorRepository.get_by_id(db, author_id)

@app.put("/authors/{author_id}", response_model=schemas.AuthorResponse)
def update_author(author_id: int, author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return AuthorRepository.update(db, author_id, author)

@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    return AuthorRepository.delete(db, author_id)

# Эндпоинты для книг
@app.post("/books", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return BookRepository.create(db, book)

@app.get("/books", response_model=List[schemas.BookResponse])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return BookRepository.get_all(db, skip, limit)

@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    return BookRepository.get_by_id(db, book_id)

@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    return BookRepository.update(db, book_id, book)

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return BookRepository.delete(db, book_id)

# Эндпоинты для выдач книг
@app.post("/borrows", response_model=schemas.BorrowResponse)
def create_borrow(borrow: schemas.BorrowCreate, db: Session = Depends(get_db)):
    return BorrowRepository.create(db, borrow)

@app.get("/borrows", response_model=List[schemas.BorrowResponse])
def read_borrows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return BorrowRepository.get_all(db, skip, limit)

@app.get("/borrows/{borrow_id}", response_model=schemas.BorrowResponse)
def read_borrow(borrow_id: int, db: Session = Depends(get_db)):
    return BorrowRepository.get_by_id(db, borrow_id)

@app.patch("/borrows/{borrow_id}/return", response_model=schemas.BorrowResponse)
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    return BorrowRepository.return_book(db, borrow_id)

