from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from . import config

_pw = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(literal_pw: str):
    return _pw.hash(literal_pw)


def verify_password(literal_pw: str, hashed_pw: str):
    return _pw.verify(literal_pw, hashed_pw)


def create_access_token(sub: str):
    exp_date = datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    payload = {"sub": sub, "exp": exp_date}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALG)
