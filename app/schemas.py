from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class FileIn(BaseModel):
    filename: str
    size_b: int
    content_type: Optional[str] = None
    key: str


class FileOut(BaseModel):
    id: int
    filename: str
    size_b: int
    content_type: Optional[str] = None
    created_at: datetime
    key: str

    class Config:
        from_attributes = True


class FileList(BaseModel):
    files: List[FileOut]
