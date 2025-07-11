# from entities import book
from .session import engine
from .base import Base
from src.entities.book import Book

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)