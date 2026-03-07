from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependecies import get_session
from datetime import datetime, timezone, timedelta
from models import Loan, Book, User, Fine, book_output,book_entry

loan_router = APIRouter(prefix="/loan", tags=["loan"])


def verify_loan(user: int, session: Session = Depends(get_session)):
    find_user = session.query(Loan).filter(User.id == user).all()
    if not find_user:
        return 0
    loan = 0
    for item in find_user:
        if item.active:
            loan += 1
    return loan


@loan_router.post("/loan")
def register_loan(days, book_id: int, user_id: int, session: Session = Depends(get_session)):
    find_book = session.query(Book).filter(Book.id == book_id).first()
    find_user = session.query(User).filter(User.id == user_id).first()

    if not find_book:
        raise HTTPException(status_code=400, detail="Book not found")
    elif not find_user:
        raise HTTPException(status_code=400, detail="User not found")
    elif verify_loan(find_user.id, session) >= 3:
        raise HTTPException(status_code=400, detail="too many Loans")

    today = datetime.now(timezone.utc)
    deadline = today + timedelta(days=days)
    final_deadline = deadline + timedelta(days=2)
    new_loan = Loan(book_id=find_book.id,book=find_book.name, user_id=find_user.user, grace_deadline=deadline,
                    final_deadline=final_deadline, loan_date=today)

    session.add(new_loan)
    session.commit()
    return {"message": "Loan added successfully",
            "user": find_user.id,
            "deadline": deadline,
            "final_deadline": final_deadline,
            }


@loan_router.post("/return_book")
def return_book(loan_id: int, session: Session = Depends(get_session)):
    find_loan = session.query(Loan).filter(Loan.user_id == loan_id).first()
    find_book = session.query(Book).filter(Book.id == find_loan.book_id).first()
    is_in_stock = True
    msg = "book returned successfully"
    if not find_loan:
        raise HTTPException(status_code=400, detail="Loan not found")
    elif not find_loan.active:
        raise HTTPException(status_code=400, detail="Loan already solved")

    if not find_book:
        is_in_stock = False

    if find_loan.final_deadline < datetime.now(timezone.utc):
        today = datetime.now(timezone.utc)
        day = find_loan.final_deadline - today
        fine = 2.0 * day.days
        new_fine = Fine(book_id=find_loan.book_id,user_id=find_loan.user_id,date=today,fine=fine)
        session.add(new_fine)
        new_entry = book_entry (book=find_loan.book,book_id=find_book.book_id,date=)





