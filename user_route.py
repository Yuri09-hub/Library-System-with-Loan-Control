from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from main import bcrypt_context
from models import User
from dependecies import get_session
from schemas import Userschemas
from data_verification import email_validation, number_validation

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/User")
async def User():
    return {"User route created"}


@user_router.post("/User/Create")
async def Create_user(user_schema: Userschemas, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    if email_validation(user_schema.email):
        raise HTTPException(status_code=400, detail="Email is not valid")
    elif number_validation(user_schema.phone):
        raise HTTPException(status_code=400, detail="Phone number is not valid")

    encrypted_password = bcrypt_context.hash(user_schema.password)
    new_user = User(name=user_schema.name.title(), email=user_schema.email, passwor=encrypted_password,
                    phone=user_schema.phone)
    session.add(new_user)
    session.commit()

    user = session.query(User).filter(User.id == 1).first()
    if user:
        user.admin = True
        session.commit()

    return {"User created"}
