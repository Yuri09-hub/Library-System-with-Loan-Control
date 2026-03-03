from sqlalchemy import Column, ForeignKey, Float, DateTime, Integer, String, create_engine, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Relationship


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
    phone = Column("phone", String, nullable=False)
    id_card = Column("id_card", String, nullable=False, unique=True)
    loan = Relationship("Loan", back_populates="users")

    def __init__(self, name, email, phone, id_card):
        self.name = name
        self.email = email
        self.phone = phone
        self.id_card = id_card
        self.loan_history = []


class Loan(base):
    __tablename__ = 'loans'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    book_id = Column("book_id", Integer, ForeignKey('books.id'))
    user_id = Column("user_id", Integer, ForeignKey('users.id'))
    loan_date = Column("loan_date", DateTime)
    grace_deadline = Column("grace_deadline", DateTime)
    final_deadline = Column("final_deadline", DateTime)
    active = Column("active", Boolean)

    user = Relationship("User", back_populates="loans")

    def __init__(self, book, user, loan_date, grace_deadline, final_deadline, active=True):
        self.book = book
        self.user = user
        self.loan_date = loan_date
        self.grace_deadline = grace_deadline
        self.final_deadline = final_deadline
        self.active = active


class Fine(base):
    __tablename__ = 'fines'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    book = Column("book_id", Integer, ForeignKey('books.id'))
    user = Column("user", Integer, ForeignKey('users.id'))
    date = Column("date", DateTime)
    fine = Column("fine", Float)
    active = Column("active", Boolean)

    def __init__(self, book, user, date, fine=0.0, active=True):
        self.book = book
        self.user = user
        self.date = date
        self.fine = fine
        self.active = active


base.metadata.create_all(bind=db)
