from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import schemas
from config import models
from datetime import datetime


class AuthorRepository:
    @staticmethod
    def create(db: Session, author: schemas.AuthorCreate):
        db_author = models.Author(**author.model_dump())
        try:
            db.add(db_author)
            db.commit()
            db.refresh(db_author)
            return db_author
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Author already exists")

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Author).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, author_id: int):
        author = db.query(models.Author).filter(models.Author.id == author_id).first()
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    @staticmethod
    def update(db: Session, author_id: int, author_data: schemas.AuthorCreate):
        db_author = AuthorRepository.get_by_id(db, author_id)
        for key, value in author_data.model_dump(exclude_unset=True).items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
        return db_author

    @staticmethod
    def delete(db: Session, author_id: int):
        db_author = AuthorRepository.get_by_id(db, author_id)
        db.delete(db_author)
        db.commit()
        return {"detail": "Author deleted successfully"}


class BookRepository:
    @staticmethod
    def create(db: Session, book: schemas.BookCreate):
        db_book = models.Book(**book.model_dump())
        try:
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            return db_book
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Book could not be created")

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Book).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, book_id: int):
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    @staticmethod
    def update(db: Session, book_id: int, book_data: schemas.BookCreate):
        db_book = BookRepository.get_by_id(db, book_id)
        for key, value in book_data.model_dump(exclude_unset=True).items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book

    @staticmethod
    def delete(db: Session, book_id: int):
        db_book = BookRepository.get_by_id(db, book_id)
        db.delete(db_book)
        db.commit()
        return {"detail": "Book deleted successfully"}


class BorrowRepository:
    @staticmethod
    def create(db: Session, borrow: schemas.BorrowCreate):
        book = BookRepository.get_by_id(db, borrow.book_id)
        if book.available_copies <= 0:
            raise HTTPException(status_code=400, detail="No available copies of this book")

        book.available_copies -= 1
        db_borrow = models.Borrow(**borrow.model_dump())

        try:
            db.add(db_borrow)
            db.commit()
            db.refresh(db_borrow)
            return db_borrow
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Borrow could not be created")

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Borrow).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, borrow_id: int):
        borrow = db.query(models.Borrow).filter(models.Borrow.id == borrow_id).first()
        if not borrow:
            raise HTTPException(status_code=404, detail="Borrow record not found")
        return borrow

    @staticmethod
    def return_book(db: Session, borrow_id: int):
        db_borrow = BorrowRepository.get_by_id(db, borrow_id)

        if db_borrow.return_date:
            raise HTTPException(status_code=400, detail="Book already returned")

        db_borrow.return_date = datetime.utcnow()
        book = BookRepository.get_by_id(db, db_borrow.book_id)
        book.available_copies += 1

        db.commit()
        db.refresh(db_borrow)
        return db_borrow