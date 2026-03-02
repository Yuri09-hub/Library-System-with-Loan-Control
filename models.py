from sqlalchemy import Column, ForeignKey, Float, DateTime, Integer, String, create_engine, JSON, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

db = create_engine('sqlite:///data.db')
Session = sessionmaker(bind=db)
session = Session()

base = declarative_base()


class Book(base):
    __tablename__ = 'books'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    writer = Column("writer", String, nullable=False)
    Category = Column("Category", String, nullable=False)
    isbn = Column("isbn", String, nullable=False, unique=True)
    stock = Column("stock", Integer, nullable=False)

    def __init__(self, name, writer, Category, isbn, stock):
        self.name = name
        self.writer = writer
        self.Category = Category
        self.isbn = isbn
        self.stock = stock


class User(base):
    __tablename__ = 'users'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", String)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    phone = Column("phone", String, nullable=False)
    id_card = Column("id_card", String, nullable=False, unique=True)
    loan_history = Column("loan_history", JSON, default=[])

    def __init__(self, name, email, password, phone, id_card):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.id_card = id_card
        self.loan_history = []


class Loan(base):
    __tablename__ = 'loans'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    book = Column("book_id", Integer, ForeignKey('books.id'))
    user = Column("user", Integer, ForeignKey('users.id'))
    loan_date = Column("loan_date", DateTime)
    expected_return_date = Column("expected_return_date", DateTime)
    actual_return_date = Column("actual_return_date", DateTime)
    active = Column("active", Boolean)

    def __init__(self, book, user, loan_date, expected_return_date, actual_return_date):
        self.book = book
        self.user = user
        self.loan_date = loan_date
        self.expected_return_date = expected_return_date
        self.actual_return_date = actual_return_date


class Fine(base):
    __tablename__ = 'fines'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    book = Column("book_id", Integer, ForeignKey('books.id'))
    user = Column("user", Integer, ForeignKey('users.id'))
    date = Column("date", DateTime)
    fine = Column("fine", Float)
    active = Column("active", Boolean)

    def __init__(self, book, user, date, fine=2.0):
        self.book = book
        self.user = user
        self.date = date
        self.fine = fine


base.metadata.create_all(bind=db)
