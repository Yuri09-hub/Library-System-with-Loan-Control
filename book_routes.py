from fastapi import APIRouter, Depends, HTTPException
from models import book_entry, book_output, Book, User
from schemas import Bookschemas
from dependecies import get_session, verify_token
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from data_verification import is_valid_isbn13

book_router = APIRouter(prefix="/book", tags=["book"])


@book_router.post("/Add_book")
def add_book(book_schemas: Bookschemas, session: Session = Depends(get_session),
             user: User = Depends(verify_token)):
    verify_book = session.query(Book).filter(Book.isbn == book_schemas.isbn).first()

    if verify_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    if not is_valid_isbn13(book_schemas.isbn):
        raise HTTPException(status_code=400, detail="ISBN not valid")
    if not user.admin:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")

    new_book = Book(name=book_schemas.name.title(), isbn=book_schemas.isbn,
                    writer=book_schemas.writer.title(), category=book_schemas.category.title())

    session.add(new_book)
    session.flush()

    new_entry = book_entry(book=new_book.name, book_id=new_book.id,
                           date=datetime.now(timezone.utc), amount=book_schemas.amount)
    session.add(new_entry)
    session.commit()

    return {
        "message": "Book added successfully"
    }
