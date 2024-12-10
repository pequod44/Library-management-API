from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    birth_date = Column(Date)

    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    available_copies = Column(Integer, default=1)
    author_id = Column(Integer, ForeignKey('authors.id'))

    author = relationship("Author", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")


class Borrow(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    reader_name = Column(String)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="borrows")