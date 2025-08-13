from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    plain_password: str


class UserLogin(BaseModel):
    username: str
    plain_password: str
