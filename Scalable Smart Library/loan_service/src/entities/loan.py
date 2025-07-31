from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy import func
from src.database.base import Base

class LoanStatus(PyEnum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"


class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    book_id = Column(Integer, nullable=False)
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=False)
    return_date = Column(DateTime(timezone=True), nullable=True)
    extended_due_date = Column(DateTime(timezone=True), nullable=True)
    extension_count = Column(Integer, nullable=False, default=0)
    status = Column(Enum(LoanStatus), nullable=False, default=LoanStatus.ACTIVE)
    

    def __repr__(self):
        return f"<Loan(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, status={self.status})>"