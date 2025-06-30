from fastapi import FastAPI
from src.controllers.controller import router as books_router

def register_routers(app: FastAPI):
    app.include_router(books_router)
