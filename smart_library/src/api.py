from fastapi import FastAPI
from src.users.controller import router as users_router
from src.books.controller import router as books_router
from src.loans.controller import router as loans_router

def register_routers(app: FastAPI):
    app.include_router(users_router)
    app.include_router(books_router)
    app.include_router(loans_router)