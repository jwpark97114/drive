import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from . import config


DB_USER = os.getenv("MYSQL_USER")
DB_PASS = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT")
DB_NAME = os.getenv("MYSQL_DB")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

Base = declarative_base()

session_local = sessionmaker(bind=engine, autocommit=False, autoflush=False)
