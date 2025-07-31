from pydantic import BaseModel, Field


class AddBook(BaseModel):
    title: str
    author: str
    isbn: str
    copies: int

class UpdateBook(BaseModel):
    copies: int
    available_copies: int


class BookOverview(BaseModel):
    total_books: int
    books_available: int
    books_borrowed: int
