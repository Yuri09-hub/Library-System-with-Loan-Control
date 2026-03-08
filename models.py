from sqlalchemy import Column, ForeignKey, Float, DateTime, Integer, String, create_engine, Boolean
from sqlalchemy.orm import declarative_base

db = create_engine('sqlite:///data.db')

base = declarative_base()


class Book(base):
    __tablename__ = 'books'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    writer = Column("writer", String, nullable=False)
    category = Column("category", String, nullable=False)
    isbn = Column("isbn", String, nullable=False, unique=True)

    def __init__(self, name, writer, category, isbn):
        self.name = name
        self.writer = writer
        self.category = category
        self.isbn = isbn


class book_entry(base):
    __tablename__ = 'book_entry'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    book = Column("book", String, nullable=False)
    book_id = Column("book_id", ForeignKey("books.id"), nullable=False)
    amount = Column("amount", Integer, nullable=False)
    date = Column("date", DateTime, nullable=False)

    def __init__(self, book, book_id, amount, date):
        self.book = book
        self.book_id = book_id
        self.amount = amount
        self.date = date


class book_output(base):
    __tablename__ = "book_output"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    book = Column("book", String, nullable=False)
    book_id = Column("book_id", ForeignKey("books.id"), nullable=False)
    amount = Column("amount", Integer, nullable=False)
    date = Column("date", DateTime, nullable=False)

    def __init__(self, book, book_id, date,amount):
        self.book = book
        self.book_id = book_id
        self.date = date
        self.amount = amount


class User(base):
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    password = Column("password", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    phone = Column("phone", String, nullable=False, unique=True)
    id_card = Column("id_card", String, nullable=False, unique=True)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, nullable=False)

    def __init__(self, name, password, email, phone, id_card):
        self.name = name
        self.email = email
        self.phone = phone
        self.id_card = id_card
        self.password = password
        self.active = True
        self.admin = False


class Loan(base):
    __tablename__ = 'loans'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    book = Column("name", String, nullable=False)
    book_id = Column("book_id", Integer, ForeignKey('books.id'))
    user_id = Column("user_id", Integer, ForeignKey('users.id'))
    loan_date = Column("loan_date", DateTime)
    expected_deadline = Column("expected_deadline", DateTime)
    final_deadline = Column("final_deadline", DateTime)
    active = Column("active", Boolean)

    def __init__(self, book, book_id, user_id, loan_date, grace_deadline, final_deadline):
        self.book = book
        self.book_id = book_id
        self.user_id = user_id
        self.loan_date = loan_date
        self.expected_deadline = grace_deadline
        self.final_deadline = final_deadline
        self.active = True


class Fine(base):
    __tablename__ = 'fines'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    book_id = Column("book_id", Integer, ForeignKey('books.id'))
    user_id = Column("user", Integer, ForeignKey('users.id'))
    date = Column("date", DateTime)
    fine = Column("fine", Float)
    active = Column("active", Boolean)

    def __init__(self, book_id, user_id, date, fine=0.0):
        self.book = book_id
        self.user_id = user_id
        self.date = date
        self.fine = fine
        self.active = True
