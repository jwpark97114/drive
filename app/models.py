from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(512), unique=True, nullable=False, index=True)
    hashed_password = Column(String(512), nullable=False)


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    key = Column(String(512), nullable=False, index=True)
    filename = Column(String(256), nullable=False)
    size_b = Column(Integer, default=0)
    content_type = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    owner = relationship("User", backref="files")
    __table_args__ = (
        UniqueConstraint("owner_user_id", "key", name="owner_id_key_constraint"),
    )
