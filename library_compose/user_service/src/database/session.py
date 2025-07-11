from typing import Annotated
from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')  

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_async_engine(
    DATABASE_URL,
    echo = True,
    future=True
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

@asynccontextmanager   # controller er depends theke bachte eto kahini kora laglo
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
