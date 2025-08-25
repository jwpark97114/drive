from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import UserCreate, UserOut, Token, UserLogin, FileIn, FileList, FileOut
from ..models import User, File
from ..depends import get_db, get_current_user
from ..auth import hash_password, verify_password, create_access_token
from typing import List
from ..utils.s3 import presign_get, presign_put

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(new_user: UserCreate, db: Session = Depends(get_db)):
    user_exist = db.execute(
        select(User).where(User.email == new_user.email)
    ).scalar_one_or_none()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already exist in the system")

    user = User(email=new_user.email, hashed_password=hash_password(new_user.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.execute(
        select(User).where(User.email == user_login.email)
    ).scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
        )
    token = create_access_token(sub=user.email)
    return {"access_token": token, "token_type": "bearer"}


def authenticate(db: Session, username: str, password: str):
    # If you use email as the username, just treat `username` as email here.
    user = db.execute(select(User).where(User.email == username)).scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


@router.post("/login_token", response_model=Token)  # OAuth2 password flow for Swagger
def login_form(
    form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate(db, form.username, form.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(sub=str(user.email))
    return {"access_token": token, "token_type": "bearer"}
