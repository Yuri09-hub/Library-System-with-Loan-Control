from models import User, Loan, Fine, Book, session
from sqlalchemy.exc import IntegrityError
from data_verification import *
from datetime import datetime, timedelta, timezone


class Library:

    @staticmethod
    def register_book(name:str, writer:str, Category:str, isbn:str, stock:int):
        try:
            if not is_valid_isbn13(isbn):
                return "ISBN is not valid"
            else:

                book = Book(name.title(), writer.title(), Category.title(), isbn, stock)
                session.add(book)
                session.commit()
                session.close()
                return "Book added successfully"
        except IntegrityError as e:
            return f" Error: {e}"

    @staticmethod
    def register_user(name: str, email: str, phone: str, id_card: str):
        try:
            if not email_validation(email):
                return "Email is not invalid"
            elif not number_validation(phone):
                return "number phone is not valid"
            else:
                user = User(name=name.title(), email=email, phone=phone, id_card=id_card)
                session.add(user)
                session.commit()
                session.close()
                return "User created successfully"
        except IntegrityError as e:
            return f" Error: {e}"

    @staticmethod
    def register_loan(book, user, expected_day):
        count = 0
        try:
            verify_book = session.query(Book).filter(book == Book.id).first()
            verify_loan = session.query(Loan).filter(Loan.user == user).all()
            verify_user = session.query(User).filter(User.id == user.id).first()
            for item in verify_loan:
                if item.active is True:
                    count = count + 1

            if not verify_book:
                return "Book not found"
            elif count >= 3:
                return "Too many loans"
            elif not verify_user:
                return "User not found"

            loan_date = datetime.now(timezone.utc)
            expected_deadline = timedelta(days=expected_day)
            actual_deadline = timedelta(days=expected_day + 2)

            new_loan = Loan(book=book, user=user, loan_date=loan_date, expected_return_date=expected_deadline,
                            actual_return_date=actual_deadline,)
            session.add(new_loan)
            session.commit()
            session.close()
            return "Loan added successfully"
        except IntegrityError as e:
            return f" Error: {e}"

    @staticmethod
    def view_books():
        try:
            books = session.query(Book).all()
            for book in books:
                print(
                    f"{book.id:<5}{book.name:<20}{book.writer:<20}{book.Category:<15}{book.isbn:<20}{book.stock:<10}")

            print("-" * 100)
        except IntegrityError as e:
            print(f"Error: {e}")

    @staticmethod
    def view_users():
        try:
            user = session.query(User).all()
            for users in user:




