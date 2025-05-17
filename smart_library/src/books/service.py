from .models import AddBook,  BookOverview
from src.entities.book import Book
from sqlalchemy import select
from sqlalchemy import select, or_, func
from src.database.session import get_db


async def add_book(title, author, isbn, copies):
    new_book = Book(title=title, author=author, isbn=isbn, copies=copies, available_copies=copies)

    async with get_db() as db:
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
    return new_book


async def get_book(id):
    async with get_db() as db:
        result = await db.execute(select(Book).where(Book.id == id))
        book = result.scalars().first()
    if book is None:
        return None
    return book


async def search_books(search_term):
    # ILIKE for case-insensitive search
    async with get_db() as db:
        stmt = select(Book).where(
            or_(
                Book.title.ilike(f"%{search_term}%"),
                Book.author.ilike(f"%{search_term}%"),
                # Book.description.ilike(f"%{search_term}%")  # Optional
            )
        )
        result = await db.execute(stmt)
    return result.scalars().all()


async def update_book(id, copies, available_copies):
    async with get_db() as db:
        book = await db.execute(select(Book).where(Book.id == id))
        book = book.scalars().first()
        if not book:
            return None
        book.copies = copies
        book.available_copies = available_copies
        await db.commit()
        await db.refresh(book)
    return book


async def delete_book(id):
    async with get_db() as db:
        book = await db.execute(select(Book).where(Book.id == id))
        book = book.scalars().first()
        if not book:
            return None
        await db.delete(book)
        await db.commit()
    return {"detail": "Book deleted successfully"}


async def update_borrowed_count(book_id):
    async with get_db() as db:
        book = await db.execute(select(Book).where(Book.id == book_id))
        book = book.scalars().first()
        if not book:
            return None
        book.borrowed_count += 1
        await db.commit()
        await db.refresh(book)
    return book


async def get_popular_books():
    async with get_db() as db:
        result = await db.execute(
            select(Book).order_by(Book.borrowed_count.desc()).limit(5)
        )
        books = result.scalars().all()
    return books


async def books_overview():
    async with get_db() as db:
        books = await db.execute(select(Book))
        books = books.scalars().all()
        total_books = 0
        for book in books:
            total_books += book.copies

        total_available_books = 0
        for book in books:
            total_available_books += book.available_copies

        total_borrowed_books = total_books - total_available_books
        
    return BookOverview(
        total_books=total_books,
        books_available=total_available_books,
        books_borrowed=total_borrowed_books
    )