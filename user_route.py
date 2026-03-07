from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from main import becrypt_context, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTE, ALGORITHM
from models import User
from dependecies import get_session, verify_token
from schemas import Userschemas, LoginSchema
from data_verification import email_validation, number_validation
from datetime import datetime, timedelta, timezone
from jose import jwt

user_router = APIRouter(prefix="/user", tags=["user"])


def creat_token(id: int, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)):
    expiration_date = datetime.now(timezone.utc) + duration_token
    dict_info = {"sub": str(id), "exp": expiration_date.timestamp()}
    jwt_token = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return jwt_token


def authenticate_user(email, password, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not becrypt_context.verify(password, user.password):
        return False
    else:
        return user


@user_router.post("/Create")
async def Create_Account(user_schema: Userschemas, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    if email_validation(user_schema.email):
        raise HTTPException(status_code=400, detail="Email is not valid")
    elif number_validation(user_schema.phone):
        raise HTTPException(status_code=400, detail="Phone number is not valid")

    encrypted_password = becrypt_context.hash(user_schema.password)
    new_user = User(name=user_schema.name.title(), email=user_schema.email, password=encrypted_password,
                    phone=user_schema.phone, id_card=user_schema.id_card)
    session.add(new_user)
    session.flush()

    user = session.query(User).filter(User.id == 1).first()
    if user:
        user.admin = True

    session.commit()
    return {"Account created successfully."}


@user_router.post("/Login")
async def Login(login: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login.email, login.password, session)

    if not user:
        raise HTTPException(status_code=400, detail="User does not exist or invalid credentials")
    else:
        access_token = creat_token(user.id)
        refresh_token = creat_token(user.id, duration_token=timedelta(days=10))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }


@user_router.post("/Login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist or invalid credentials")
    else:
        access_token = creat_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer",
        }


@user_router.get("/Refresh_token")
async def refresh_token(user: User = Depends(verify_token)):
    access_token = creat_token(user.id)
    return {
        "access_token": access_token,
        "type": "Bearer",
    }


@user_router.post("/Make_admin")
def make_admin(user_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if user.id == 1:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")

    find_user = session.query(User).filter(User.id == user_id).first()
    if not find_user:
        raise HTTPException(status_code=404, detail="User not found")

    find_user.admin = True

    return {
        "message": "User successfully promoted to admin.",
        "user": find_user.id
    }


@user_router.post("/Remove_admin")
def remove_admin(user_id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if user.id == 1:
        raise HTTPException(status_code=401, detail="You do not have permission to make this change.")

    find_user = session.query(User).filter(User.id == user_id).first()
    if not find_user:
        raise HTTPException(status_code=404, detail="User not found")

    find_user.admin = False
    return {"message": "Admin privileges removed successfully",
            "user": find_user.id
    }
