from src.database.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy import func
from enum import Enum as PyEnum

class UserRole(PyEnum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, role={self.role})>"
    