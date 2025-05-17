from .session import engine
from .base import Base
from src.entities import user, book, loan

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)