from models import User, Loan, Fine, Book
from sqlalchemy.exc import IntegrityError
from data_verification import *
from datetime import datetime, timedelta


def number_of_loans_in_arrears(user, session):
    verify = session.query(Loan).filter(Loan.user == user, Loan.active == True,
                                        Loan.final_deadline < datetime.now()).count()
    if verify == 0:
        return 0
    return verify


class Library:
    @staticmethod
    def register_book(name: str, writer: str, Category: str, isbn: str, stock: int, session):
        if not is_valid_isbn13(isbn):
            return "ISBN is not valid"
        book = Book(name.title(), writer.title(), Category.title(), isbn, stock)
        session.add(book)
        return "Book added successfully"

    @staticmethod
    def register_user(name: str, email: str, phone: str, id_card: str, session):
        if not email_validation(email):
            return "Email is not invalid"
        elif not number_validation(phone):
            return "number phone is not valid"
        else:
            user = User(name=name.title(), email=email, phone=phone, id_card=id_card)
            session.add(user)
            return "User created successfully"

    @staticmethod
    def register_loan(book, user, number_days, session):
        count = number_of_loans_in_arrears(user, session)

        if count >= 3:
            return ("Due to the number of overdue loans, your account is not "
                    "permitted to take out any more loans. ")
        number_loan = 0
        # verify user
        found_user = session.query(User).filter(User.id == user).first()
        # verify book
        found_book = session.query(Book).filter(Book.id == book).first()
        # verify all user loan
        found_loan = session.query(Loan).filter(Loan.user == user).all()

        for item in found_loan:
            if item.active is True:
                number_loan += 1

        if not found_book or found_book.stock == 0:
            return "Book not found or out of stock"
        elif not found_user:
            return "User not found"
        elif number_loan >= 3:
            return "Too many loans"

        loan_date = datetime.now()
        grace_deadline = loan_date + timedelta(days=number_days)
        final_deadline = grace_deadline + timedelta(days=2)

        new_loan = Loan(book=book, user=user, loan_date=loan_date, final_deadline=final_deadline,
                        grace_deadline=grace_deadline)
        session.add(new_loan)
        informatio = [f"Book:{found_book.name}-date:{new_loan.loan_date}"]
        found_user.loan_history.append(informatio)
        found_book.stock -= 1
        return "Loan added successfully"

    @staticmethod
    def return_book(user, id_book, session):
        today = datetime.now()
        book_found = session.query(Book).filter(Book.id == id_book).first()
        loan_found = session.query(Loan).filter(Loan.user == user, Loan.book == id_book,
                                                Loan.active == True).first()

        if not book_found:
            return "Book not found"
        elif not loan_found:
            return "Loan not found"

        if loan_found.final_deadline < today:
            value = today - loan_found.final_deadline
            pay = value.days * 2.0
            fine = Fine(book=id_book, user=user, date=today, fine=pay)
            session.add(fine)
            loan_found.active = False
            book_found.stock += 1
            return f"The book has been returned, due to the delay(s), you will be fined .{pay}"
        else:
            loan_found.active = False
            book_found.stock += 1
            return f"The book was returned within its business days."

    @staticmethod
    def pay_fines(user, session):
        found_fine = session.query(Fine).filter(Fine.user == user).all()
        if not found_fine:
            return "Fine not found"

        for fine in found_fine:
            fine.active = False

        return f"Fines paid"

    @staticmethod
    def search_book(choice: int, session, Answer:str):
        if choice == 1:
            books = session.query(Book).filter(Book.name == Answer).all()
            if not books:
                print("Book not found")
            for book in books:
                print(
                    f"{book.id:<5}{book.name:<20}{book.writer:<20}{book.Category:<15}{book.isbn:<20}{book.stock:<10}")

            print("-" * 100)

        elif choice == 2:
            books = session.query(Book).filter(Book.writer == Answer).all()
            if not books:
                print("Book not found")
            for book in books:
                print(
                    f"{book.id:<5}{book.name:<20}{book.writer:<20}{book.Category:<15}{book.isbn:<20}{book.stock:<10}")

            print("-" * 100)

        elif choice == 3:
            books = session.query(Book).filter(Book.Category == Answer).all()
            if not books:
                print("Book not found")
            for book in books:
                print(
                    f"{book.id:<5}{book.name:<20}{book.writer:<20}{book.Category:<15}{book.isbn:<20}{book.stock:<10}")

            print("-" * 100)

    @staticmethod
    def view_books(session):
        try:
            books = session.query(Book).all()
            for book in books:
                print(
                    f"{book.id:<5}{book.name:<20}{book.writer:<20}{book.Category:<15}{book.isbn:<20}{book.stock:<10}")

            print("-" * 100)
        except IntegrityError as e:
            print(f" fun.view_books- Error: {e}")

    @staticmethod
    def view_users(session):
        try:
            users = session.query(User).all()
            if not users:
                print("Users not found")
            for user in users:
                print(f"{user.id:<5}"
                      f"{user.name:<20}"
                      f"{user.email:<25}"
                      f"{user.phone:<15}"
                      f"{user.id_card:<20}")
                print("-" * 120)
        except IntegrityError as e:
            print(f" fun. view_users - Error: {e}")

    @staticmethod
    def view_all_loan(session):
        loans = session.query(Loan).all()
        if not loans:
            print(' Loan not found')
        for loan in loans:
            print(f"{loan.id:<5}{loan.book:<10}{loan.user:<10}"
                  f"{str(loan.loan_date):<20}"
                  f"{str(loan.grace_deadline):<20}"
                  f"{str(loan.final_deadline):<20}"
                  f"{str(loan.active):<10}")
