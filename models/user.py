from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel

DATABASE_URL = "mysql+aiomysql://root:n301k399f27@127.0.0.1/drive"

Base = declarative_base

engine = create_async_engine(url=DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique = True)
    email = Column(String(200))
    hashed_password = Column(String(1024))
    quota_bytes = Column(Integer)
    used_bytes = Column(Integer)


