from fastapi import FastAPI
from passlib.context import CryptContext
from user_route import user_router
from loan_route import loan_router
from book_routes import book_router
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

app.include_router(user_router)
app.include_router(loan_router)
app.include_router(book_router)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
