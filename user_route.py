from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from main import bcrypt_context
from models import User
from dependecies import get_session
from schemas import Userschemas

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/User")
async def User():
    return {"User route created"}


@user_router.post("/User/Create")
async def Create_user(user_schema: Userschemas, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")



