from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from src.books.models import AddBook, UpdateBook
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.database.session import get_db
from . import service


router = APIRouter(
    prefix="/api/v1/books",
    tags=["Books"],
)

@router.post("/")
async def add_book(book: AddBook):
    return await service.add_book(book.title, book.author, book.isbn, book.copies)


@router.get("/{id}")
async def get_book(id: int):
    book = await service.get_book(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/")
async def search_books(search: Optional[str] = None):
    if not search:
        raise HTTPException(status_code=400, detail="Search query parameter is required")
    
    books = await service.search_books(search)
    if len(books) == 0:
        raise HTTPException(status_code=404, detail="No books found")
    return books


@router.put("/{id}")
async def update_book(id: int, book: UpdateBook):
    book = await service.update_book(id, book.copies, book.available_copies)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")


@router.delete("/{id}")
async def delete_book(id: int):
    message = await service.delete_book(id)
    if not message:
        raise HTTPException(status_code=404, detail="Book not found")
    return message

@router.get("/stats/popular")
async def get_popular_books():
    books = await service.get_popular_books()
    if len(books) == 0:
        raise HTTPException(status_code=404, detail="No books found")
    return books