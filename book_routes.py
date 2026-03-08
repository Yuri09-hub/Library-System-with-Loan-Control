from fastapi import APIRouter, Depends, HTTPException
from models import book_entry, Book, User
from schemas import Bookschemas
from dependecies import get_session, verify_token
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from data_verification import is_valid_isbn13

book_router = APIRouter(prefix="/book", tags=["book"])


@book_router.post("/Add_book")
def add_book(book_schemas: Bookschemas, amount: int, session: Session = Depends(get_session),
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
                           date=datetime.now(timezone.utc), amount=amount)
    session.add(new_entry)
    session.commit()

    return {
        "message": "Book added successfully"
    }


@book_router.post("/update_book")
async def update_book(book_id: int, book_schemas: Bookschemas, user: User = Depends(verify_token),
                      session: Session = Depends(get_session)):
    find_book = session.query(Book).filter(Book.id == book_id).first()
    if not find_book:
        raise HTTPException(status_code=404, detail="Book not found")
    elif not user.admin:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")

    if not is_valid_isbn13(book_schemas.isbn):
        raise HTTPException(status_code=400, detail="ISBN not valid")

    find_book.name = book_schemas.name.title()
    find_book.isbn = book_schemas.isbn
    find_book.writer = book_schemas.writer.title()
    find_book.category = book_schemas.category.title()
    session.commit()

    return {
        "message": "book successfully updated"
    }


@book_router.get("/view_list_of_book")
async def view_book(session: Session = Depends(get_session)):
    book = session.query(Book).limit(10).offset(10)

    if not not book:
        raise HTTPException(status_code=404, detail="No books available")
    return {"Book": book}


@book_router.get("/search_a_book")
async def search(id: int, session: Session = Depends(get_session)):
    book = session.query(Book).filter(Book.id == id).first()

    if not book:
        raise HTTPException(status_code=404, detail="No books found")
    return {"Book": book}


@book_router.post("/book/delete")
async def delete(book_id: int, user: User = Depends(verify_token), session: Session = Depends(get_session)):
    book = session.query(Book).filter(Book.id == book_id).first()

    if not user.admin:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")
    elif not book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(book)
    session.commit()

    return {"message": "Book deleted successfully"}
