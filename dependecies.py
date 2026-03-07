from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from models import db, User
from main import oauth_scheme, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError


def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verify_token(token: str = Depends(oauth_scheme), session: Session = Depends(get_session)):
    try:
        dict_info = jwt.decode(token,SECRET_KEY,ALGORITHM)
        user_id = int(dict_info["sub"])
    except JWTError as error:
        print(error)
        raise HTTPException(status_code=400, detail=f"Error")

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

