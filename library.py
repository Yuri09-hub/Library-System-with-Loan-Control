from models import User, Loan, Fine, Book, session
from sqlalchemy.exc import IntegrityError
from data_verification import *
from datetime import datetime, timedelta, timezone


class Library:

    @staticmethod
    def register_book(name: str, writer: str, Category: str, isbn: str, stock: int):
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
            elif not verify_user:
                return "User not found"
            elif count >= 3:
                return "Too many loans"

            loan_date = datetime.now(timezone.utc)
            expected_deadline = timedelta(days=expected_day)
            actual_deadline = timedelta(days=expected_day + 2)

            new_loan = Loan(book=book, user=user, loan_date=loan_date, expected_return_date=expected_deadline,
                            actual_return_date=actual_deadline, )

            session.add(new_loan)
            verify_user.loans.append(f"book: {verify_book.name}/ date:{new_loan.loan_date}")
            session.commit()
            session.close()
            return "Loan added successfully"
        except IntegrityError as e:
            return f" Error: {e}"

    @staticmethod
    def return_book(user, id_book):
        try:
            today = datetime.now(timezone.utc)
            user_found = session.query(Loan).filter(Loan.id == user, Loan.book == id_book).first()
            if not user_found:
                return "Loan not found"

            if user_found.loan_date < today:
                d = today - user_found.loan_date
                pay = d.days * 2.0
                fine = Fine(book=id_book, user=user, fine=pay, date=today)
                user_found.active = False
                session.add(fine)
                session.commit()
                session.close()
                return f"The book has been returned, due to the delay(s), you will be fined .{pay} "
            else:
                user_found.active = False
                session.commit()
                session.close()
                return f"The book was returned within its business days."

        except IntegrityError as e:
            return f" Error: {e}"

    @staticmethod
    def pay_fines(user):
        try:
            user = session.query(Fine).filter(Fine.user == user).all()
            if not user:
                return "User not found"

            for users in user:
                users.active = False
            session.commit()
            session.close()
            return f"You have paidd the fines successfully"
        except IntegrityError as e:
            return f" Error: {e}"

    @staticmethod
    def 

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
            users = session.query(User).all()
            for user in users:
                total_loans = len(user.loan_history)
                print(f"{user.id:<5}"
                      f"{user.name:<20}"
                      f"{user.email:<25}"
                      f"{user.phone:<15}"
                      f"{user.id_card:<20}"
                      f"{total_loans:<10}")
            print("-" * 120)
        except IntegrityError as e:
            print(f"Error: {e}")
