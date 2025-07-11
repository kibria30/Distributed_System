from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import func
from src.database.base import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    copies = Column(Integer, nullable=False, default=0)
    available_copies = Column(Integer, nullable=False, default=0)
    borrowed_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    
    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author}, isbn={self.isbn})>"