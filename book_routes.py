from fastapi import APIRouter, Depends, HTTPException
from models import book_entry, book_output, Book
from schemas import Bookschemas
from dependecies import get_session
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from data_verification import is_valid_isbn13

book_router = APIRouter(prefix="/book", tags=["book"])


@book_router.post("/Add_book")
def add_book(book_schemas: Bookschemas, session: Session = Depends(get_session)):
    verify_book = session.query(Book).filter(Book.isbn == book_schemas.isbn).first()
    if verify_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    new_book = Book(name=book_schemas.name, isbn=book_schemas.isbn,
                    writer=book_schemas.writer, category=book_schemas.category)

    session.add(new_book)
    session.flush()

    new_entry = book_entry(book=new_book.name, book_id=new_book.id,
                           date=datetime.now(timezone.utc))
    session.add(new_entry)
    session.commit()

    return {
        "message": "Book added successfully"
    }
